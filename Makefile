PYTHON ?= python3

.PHONY: setup run run-classic run-extended run-chaos run-gui test package clean

setup:
	./setup.sh

run:
	./run.sh --variant extended

run-classic:
	./run.sh --config configs/classic.json

run-extended:
	./run.sh --config configs/extended.json

run-chaos:
	./run.sh --config configs/chaos.json

run-gui:
	./run.sh --config configs/extended.json --renderer tk

test:
	./test.sh

package:
	@mkdir -p dist
	@$(PYTHON) -m extetris.packaging

clean:
	rm -rf build dist/*.zip *.egg-info .pytest_cache
	find . -type d \( -name "__pycache__" -o -name ".pytest_cache" -o -name ".ipynb_checkpoints" -o -name "*.egg-info" \) -prune -exec rm -rf {} +
