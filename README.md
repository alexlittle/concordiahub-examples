# concordiahub-examples

Examples for testing/demonstrating ConcordiaHub (https://github.com/alexlittle/concordiahub).


## QuickStart
Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).


1. `git clone https://github.com/alexlittle/concordiahub-examples.git`
2. `cd concordiahub-examples`
3. `uv sync`
4. `uv run python fetch_data.py` - this will download a small example on the Cleveland Heart Dataset
5. `uv run concordiahub-dash` - launches the dashboard in your browser


## Additional dataset

You can also download the MedSynth dataset example (approx 750MB). For this run:

* `uv run python fetch_data.py --dataset medsynth`

Then restart the dashboard


## Example scripts

The scripts that build the models and load them into the dashboard are in `examples/`.
Run them from the repo root as modules, e.g. `uv run python -m examples.ex01_baseline_heart`.
The LLM examples also need [Ollama](https://ollama.com).
For full explanations see the documentation: https://concordiahub.readthedocs.io/



