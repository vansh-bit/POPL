# distributions.py: Functional-OO ShapeDistribution framework
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

from abc import ABC, abstractmethod
import random


class ShapeDistribution(ABC):
    """
    Functional-OO strategy base for selecting the next ExTetromino.
    Supports higher-order combinators (.filter, .map, .blend, .conditional)
    and operator overloading (+ for linear blend, >> for pipeline transform).
    """

    def __init__(self, seed=None):
        self._seed = seed
        self.rng = random.Random(seed)

    @abstractmethod
    def available_shapes(self):
        """Return the base candidate shape list (uncloned prototypes)."""

    @abstractmethod
    def sample(self, board=None, history=None):
        """Sample and return a fresh cloned ExTetromino."""

    def sample_many(self, count, board=None, history=None):
        hist = list(history) if history is not None else []
        drawn = []
        for _ in range(count):
            piece = self.sample(board=board, history=hist)
            drawn.append(piece)
            hist.append(piece)
        return drawn

    def filter(self, predicate, seed=None):
        return FilteredDistribution(self, predicate, seed=seed if seed is not None else self._seed)

    def map(self, transform_fn, seed=None):
        return MappedDistribution(self, transform_fn, seed=seed if seed is not None else self._seed)

    def blend(self, other, weight=0.5, seed=None):
        if not 0.0 <= weight <= 1.0:
            raise ValueError(f"Blend weight must be in [0.0, 1.0], got {weight}.")
        return BlendedDistribution(
            [(self, 1.0 - weight), (other, weight)],
            seed=seed if seed is not None else self._seed,
        )

    def conditional(self, predicate_fn, other_true, other_false=None, seed=None):
        return ConditionalDistribution(
            predicate_fn=predicate_fn,
            true_dist=other_true,
            false_dist=other_false if other_false is not None else self,
            seed=seed if seed is not None else self._seed,
        )

    def __add__(self, other):
        if not isinstance(other, ShapeDistribution):
            return NotImplemented
        return self.blend(other, weight=0.5)

    def __rshift__(self, transform_fn):
        if not callable(transform_fn):
            return NotImplemented
        return self.map(transform_fn)


class UniformDistribution(ShapeDistribution):
    """Equal probability across all supplied shapes."""

    def __init__(self, shapes, seed=None):
        super().__init__(seed=seed)
        self._shapes = [s.clone() for s in shapes]
        if not self._shapes:
            raise ValueError("UniformDistribution requires at least one shape.")

    def available_shapes(self):
        return list(self._shapes)

    def sample(self, board=None, history=None):
        return self.rng.choice(self._shapes).clone()


class WeightedDistribution(ShapeDistribution):
    """Explicit weighted sampling: P(S_i) = w_i / sum(w_j)."""

    def __init__(self, shapes_or_mapping, weights=None, seed=None):
        super().__init__(seed=seed)
        if isinstance(shapes_or_mapping, dict):
            items = list(shapes_or_mapping.items())
            self._shapes = [s.clone() for s, _ in items]
            self._weights = [float(w) for _, w in items]
        elif weights is not None:
            self._shapes = [s.clone() for s in shapes_or_mapping]
            self._weights = [float(w) for w in weights]
        else:
            items = list(shapes_or_mapping)
            self._shapes = [s.clone() for s, _ in items]
            self._weights = [float(w) for _, w in items]

        if not self._shapes:
            raise ValueError("WeightedDistribution requires at least one shape.")
        if len(self._shapes) != len(self._weights):
            raise ValueError("Shapes and weights must have equal length.")
        if any(w < 0 for w in self._weights):
            raise ValueError("Weights must be non-negative.")
        if sum(self._weights) <= 0:
            raise ValueError("Sum of weights must be strictly positive.")

    @property
    def probabilities(self):
        total = sum(self._weights)
        return [w / total for w in self._weights]

    def available_shapes(self):
        return list(self._shapes)

    def sample(self, board=None, history=None):
        return self.rng.choices(self._shapes, weights=self._weights, k=1)[0].clone()


class BagDistribution(ShapeDistribution):
    """N-Bag randomizer: shuffles bag_multiplier copies of shapes without drought."""

    def __init__(self, shapes, bag_multiplier=1, seed=None):
        super().__init__(seed=seed)
        self._shapes = [s.clone() for s in shapes]
        if not self._shapes:
            raise ValueError("BagDistribution requires at least one shape.")
        if bag_multiplier < 1:
            raise ValueError("bag_multiplier must be >= 1.")
        self.bag_multiplier = int(bag_multiplier)
        self._bag = []
        self._refill()

    def _refill(self):
        self._bag = [s.clone() for _ in range(self.bag_multiplier) for s in self._shapes]
        self.rng.shuffle(self._bag)

    def available_shapes(self):
        return list(self._shapes)

    def sample(self, board=None, history=None):
        if not self._bag:
            self._refill()
        return self._bag.pop().clone()


class AdaptiveDifficultyDistribution(ShapeDistribution):
    """
    Adjusts piece weights dynamically using board distress:
      Distress = 0.5 * (H_max / H_board) + 0.35 * (Holes / 8) + 0.15 * (Bumpiness / 15)
    """

    def __init__(self, shapes, seed=None):
        super().__init__(seed=seed)
        self._shapes = [s.clone() for s in shapes]
        if not self._shapes:
            raise ValueError("AdaptiveDifficultyDistribution requires at least one shape.")

    @staticmethod
    def compute_distress(board):
        if board is None:
            return 0.0
        h_ratio = min(1.0, board.get_max_height() / max(1, board.height))
        holes_ratio = min(1.0, board.count_holes() / 8.0)
        bump_ratio = min(1.0, board.get_bumpiness() / 15.0)
        distress = 0.5 * h_ratio + 0.35 * holes_ratio + 0.15 * bump_ratio
        return max(0.0, min(1.0, distress))

    def weights_for_board(self, board=None):
        distress = self.compute_distress(board)
        weights = []
        for s in self._shapes:
            holes = s.landing_holes()
            safe_weight = 1.0 / ((1.0 + holes) ** 2)
            hard_weight = float((1 + holes) ** 2)
            w = (1.0 - distress) * hard_weight + distress * (safe_weight * 16.0)
            weights.append(max(1e-6, w))
        return weights

    def available_shapes(self):
        return list(self._shapes)

    def sample(self, board=None, history=None):
        weights = self.weights_for_board(board)
        return self.rng.choices(self._shapes, weights=weights, k=1)[0].clone()


class MarkovDistribution(ShapeDistribution):
    """First-order Markov chain over shapes: P(S_{t+1} | S_t)."""

    def __init__(self, shapes, transition_matrix=None, repeat_penalty=0.1, seed=None):
        super().__init__(seed=seed)
        self._shapes = [s.clone() for s in shapes]
        n = len(self._shapes)
        if n == 0:
            raise ValueError("MarkovDistribution requires at least one shape.")
        if transition_matrix is None:
            if n == 1:
                self.transition_matrix = [[1.0]]
            else:
                diag_p = max(0.0, min(1.0, float(repeat_penalty))) / n
                off_p = (1.0 - diag_p) / (n - 1)
                self.transition_matrix = [
                    [diag_p if i == j else off_p for j in range(n)]
                    for i in range(n)
                ]
        else:
            if len(transition_matrix) != n or any(len(row) != n for row in transition_matrix):
                raise ValueError(f"transition_matrix must be {n}x{n}.")
            self.transition_matrix = []
            for row in transition_matrix:
                row_f = [float(x) for x in row]
                if any(x < 0 for x in row_f) or sum(row_f) <= 0:
                    raise ValueError("Each Markov row must be non-negative with positive sum.")
                total = sum(row_f)
                self.transition_matrix.append([x / total for x in row_f])
        self._last_idx = None

    def available_shapes(self):
        return list(self._shapes)

    def sample(self, board=None, history=None):
        if self._last_idx is None:
            idx = self.rng.randrange(len(self._shapes))
        else:
            weights = self.transition_matrix[self._last_idx]
            idx = self.rng.choices(range(len(self._shapes)), weights=weights, k=1)[0]
        self._last_idx = idx
        return self._shapes[idx].clone()


class FilteredDistribution(ShapeDistribution):
    def __init__(self, inner, predicate, seed=None, max_attempts=1024):
        super().__init__(seed=seed)
        self.inner = inner
        self.predicate = predicate
        self.max_attempts = max_attempts
        self._filtered_pool = [s.clone() for s in inner.available_shapes() if predicate(s)]
        if not self._filtered_pool:
            raise ValueError("Filter predicate matched zero shapes.")

    def available_shapes(self):
        return list(self._filtered_pool)

    def sample(self, board=None, history=None):
        for _ in range(self.max_attempts):
            candidate = self.inner.sample(board=board, history=history)
            if self.predicate(candidate):
                return candidate
        return self.rng.choice(self._filtered_pool).clone()


class MappedDistribution(ShapeDistribution):
    def __init__(self, inner, transform_fn, seed=None):
        super().__init__(seed=seed)
        self.inner = inner
        self.transform_fn = transform_fn

    def available_shapes(self):
        return [self.transform_fn(s.clone()) for s in self.inner.available_shapes()]

    def sample(self, board=None, history=None):
        result = self.transform_fn(self.inner.sample(board=board, history=history))
        return result.clone() if hasattr(result, "clone") else result


class BlendedDistribution(ShapeDistribution):
    def __init__(self, components, seed=None):
        super().__init__(seed=seed)
        self.components = [(dist, float(w)) for dist, w in components if w > 0]
        if not self.components:
            raise ValueError("BlendedDistribution requires at least one component with positive weight.")
        self._dists = [d for d, _ in self.components]
        self._weights = [w for _, w in self.components]

    def available_shapes(self):
        seen = set()
        merged = []
        for d in self._dists:
            for s in d.available_shapes():
                if s.coords not in seen:
                    seen.add(s.coords)
                    merged.append(s)
        return merged

    def sample(self, board=None, history=None):
        chosen_dist = self.rng.choices(self._dists, weights=self._weights, k=1)[0]
        return chosen_dist.sample(board=board, history=history)


class ConditionalDistribution(ShapeDistribution):
    def __init__(self, predicate_fn, true_dist, false_dist, seed=None):
        super().__init__(seed=seed)
        self.predicate_fn = predicate_fn
        self.true_dist = true_dist
        self.false_dist = false_dist

    def available_shapes(self):
        seen = set()
        merged = []
        for s in self.true_dist.available_shapes() + self.false_dist.available_shapes():
            if s.coords not in seen:
                seen.add(s.coords)
                merged.append(s)
        return merged

    def sample(self, board=None, history=None):
        branch = self.true_dist if self.predicate_fn(board, history) else self.false_dist
        return branch.sample(board=board, history=history)
