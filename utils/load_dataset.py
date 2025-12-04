import sys
import json
import uuid
from datasets import load_dataset
from core.retriever import Retriever
from tqdm import tqdm
import math

def load_jsonl(path, max_samples=200, collection="local_data"):
    retriever = Retriever(collection_name=collection)
    ids, docs, metas = [], [], []

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(tqdm(lines, desc=f"📥 Loading {path}", unit="lines")):
        try:
            data = json.loads(line)
            text = data.get("text")
            meta = data.get("metadata", {})
            if not text:
                continue

            ids.append(str(uuid.uuid4()))
            docs.append(text)

            clean_meta = {k: (", ".join(v) if isinstance(v, list) else str(v)) for k, v in meta.items()}
            metas.append(clean_meta)

            if max_samples and max_samples > 0 and len(ids) >= max_samples:
                break
        except Exception as e:
            print(f"⚠️ Skipping line {i} due to error: {e}")

    if ids:
        retriever.add_documents(ids, metas, docs)
        print(f"\n✅ Loaded {len(ids)} documents from {path}")
    else:
        print("\n⚠️ No valid documents loaded.")

def load_hf_dataset(name, split="train", config=None, text_field=None, max_samples=200):
    print(f"📥 Loading dataset: {name}, config={config}, split={split}")

    if config and config != "default":
        ds = load_dataset(name, name=config, split=split)
    else:
        ds = load_dataset(name, split=split)

    print("🔑 Columns available:", ds.column_names)

    if not text_field:
        candidates = ["text", "content", "sentence", "review", "question"]
        for c in candidates:
            if c in ds.column_names:
                text_field = c
                break
    if not text_field:
        text_field = ds.column_names[0]
        print(f"⚠️ No text_field specified, defaulting to first column: {text_field}")

    collection_name = name.replace("/", "_")
    retriever = Retriever(collection_name=collection_name)

    ids, docs, metas = [], [], []
    count = 0
    for row in tqdm(ds, desc=f"📦 Processing {name}", unit="rows"):
        text = row.get(text_field) if isinstance(row, dict) else getattr(row, text_field, None)
        if not text:
            continue

        ids.append(str(uuid.uuid4()))
        docs.append(text)
        clean_meta = {k: (", ".join(v) if isinstance(v, list) else str(v)) for k, v in row.items() if k != text_field}
        metas.append(clean_meta)

        count += 1
        if max_samples and max_samples > 0 and count >= max_samples:
            break

        if len(ids) >= 5000:
            retriever.add_documents(ids, metas, docs)
            print(f"✅ Inserted {count} / ~{len(ds)} docs")
            ids, docs, metas = [], [], []

    if ids:
        retriever.add_documents(ids, metas, docs)

    print(f"\n✅ Loaded {count} documents from {name}:{split}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python load_dataset.py data/knowledge.jsonl")
        print("  python load_dataset.py <dataset_name> [split] [config] [max_samples|'all']")
        sys.exit(1)

    arg = sys.argv[1]
    split = sys.argv[2] if len(sys.argv) > 2 else "train"
    config = sys.argv[3] if len(sys.argv) > 3 else None
    max_samples_arg = sys.argv[4] if len(sys.argv) > 4 else "200"

    max_samples = None
    if max_samples_arg is None or max_samples_arg.lower() in ("", "200"):
        max_samples = 200
    elif max_samples_arg.lower() in ("0", "all", "-1", "none"):
        max_samples = None
    else:
        try:
            max_samples = int(max_samples_arg)
        except Exception:
            max_samples = 200

    if arg.endswith(".jsonl"):
        load_jsonl(arg, max_samples=max_samples)
    else:
        load_hf_dataset(arg, split=split, config=config, max_samples=max_samples)
