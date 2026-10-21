"""
Downloads the example data from Hugging Face into the data/, cache/ and
data_store/ folders in the root of this repo.

On Hugging Face the data is split by example dataset, then by type:

    heart/data/...         ->  data/...
    heart/cache/...        ->  cache/heart/...
    heart/data_store/...   ->  data_store/...

(and the same for medsynth). Files that already exist are skipped, so it is
safe to re-run.

Usage:
    uv run python fetch_data.py                      # heart only (small)
    uv run python fetch_data.py --dataset medsynth   # ~740 MB
    uv run python fetch_data.py --dataset all
"""

import argparse
import shutil
import tempfile
from pathlib import Path

from huggingface_hub import hf_hub_download, list_repo_files

REPO_ID = "alexlittle/concordiahub-examples-data"
# Pin to a tag or commit hash to keep the data in step with the code
REVISION = "main"

DATASETS = ["heart", "medsynth"]
ROOT = Path(__file__).resolve().parent


def destination(dataset: str, repo_path: str, dest_root: Path) -> Path | None:
    """
    Works out where a file in the Hugging Face repo should be placed locally

    Args:
        dataset (str): dataset name, e.g. heart
        repo_path (str): path of the file within the Hugging Face repo
        dest_root (Path): root folder that data/, cache/ and data_store/ go in

    Returns:
        Path | None: local path, or None if the file is not part of the dataset
    """
    parts = Path(repo_path).parts
    if len(parts) < 3 or parts[0] != dataset:
        return None
    kind, rest = parts[1], Path(*parts[2:])
    if kind in ("data", "data_store"):
        return dest_root / kind / rest
    if kind == "cache":
        # the example scripts read ./cache/<dataset>/<model dir>/...
        return dest_root / "cache" / dataset / rest
    return None


def fetch(dataset: str, dest_root: Path) -> None:
    """
    Downloads the files for one dataset, skipping any that already exist

    Args:
        dataset (str): dataset name, e.g. heart
        dest_root (Path): root folder that data/, cache/ and data_store/ go in
    """
    files = [
        (f, destination(dataset, f, dest_root))
        for f in list_repo_files(REPO_ID, repo_type="dataset", revision=REVISION)
    ]
    files = [(f, dest) for f, dest in files if dest is not None]
    if not files:
        raise SystemExit(f"No files found for '{dataset}' in {REPO_ID}@{REVISION}")

    downloaded = skipped = 0
    for i, (repo_path, dest) in enumerate(files, start=1):
        if dest.exists():
            skipped += 1
            continue
        print(f"[{dataset} {i}/{len(files)}] {dest.relative_to(dest_root)}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=dest_root) as tmp:
            # Hugging Face verifies the file hash as it downloads
            fetched = hf_hub_download(
                REPO_ID,
                repo_path,
                repo_type="dataset",
                revision=REVISION,
                local_dir=tmp,
            )
            shutil.move(fetched, dest)
        downloaded += 1

    print(f"{dataset}: {downloaded} downloaded, {skipped} already present")


def main() -> None:
    """
    Parse arguments and download the requested datasets
    """
    parser = argparse.ArgumentParser(description="Download the ConcordiaHub example data")
    parser.add_argument(
        "--dataset",
        choices=DATASETS + ["all"],
        default="heart",
        help="which example dataset to download (default: heart)",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=ROOT,
        help="folder to put data/, cache/ and data_store/ in (default: this repo's root)",
    )
    args = parser.parse_args()

    for dataset in DATASETS if args.dataset == "all" else [args.dataset]:
        fetch(dataset, args.dest.resolve())


if __name__ == "__main__":
    main()
