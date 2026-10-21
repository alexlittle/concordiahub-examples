import os

from pathlib import Path


# all data lives in the root of this repo, whichever directory a script is run from
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CACHE_DIR = ROOT / "cache"
DATA_STORE_DIR = ROOT / "data_store"
# Must be set before concordiahub is imported
os.environ.setdefault("CONCORDIAHUB_DATA_DIR", str(DATA_STORE_DIR))

# set dir for output of perf results
PERF_OUT_DIR = ROOT / "perf_results"
PERF_OUT_DIR.mkdir(parents=True, exist_ok=True)


# General config
INSTANCE_UUID_COL = "instance_uuid"
LLM_TEMPLATE_DIR = Path(__file__).resolve().parent / "prompt_templates"


# Config for cleveland heart data
HEART_INPUT_FILE = DATA_DIR / "cleveland-heart-data.csv"
#HEART_OLLAMA_MODEL = "llama3.1:8b"
#HEART_OLLAMA_MODEL = "qwen2.5:14b-instruct-q8_0"
HEART_OLLAMA_MODEL = "gemma3:27b-it-qat"


# Config for Medsynth
MEDSYNTH_FULL_FILE = DATA_DIR / "medsynth_data_full.csv"

