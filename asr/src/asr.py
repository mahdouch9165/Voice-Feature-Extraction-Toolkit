# -*- coding: utf-8 -*-
"""ASR Evaluation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Tbdwxr_dQO-JdVhnLKACq1URBwDlGXMe
"""

from pathlib import Path
import json
import sys
import importlib.util

import datasets
import transformers
import evaluate

output_base_dir = Path("/output")
load_scripts_base_dir = Path("/app/load_scripts")

def main(model_id: str, dataset_id: str, dataset_config_name: str, dataset_split: str):
    
    output_dir = output_base_dir / (model_id.replace("/", "_") + " on " + dataset_id.replace("/", "_"))
    output_dir.mkdir(parents=True, exist_ok=True)

    sys.path.append(str(load_scripts_base_dir / "datasets" / dataset_id))
    import dataset_loader
    dataset = dataset_loader.load(dataset_config_name, dataset_split)

    sys.path.append(str(load_scripts_base_dir / "models" / model_id))
    import model_loader
    model = model_loader.load()

    predictions = model(dataset.select_columns("audio"))

    predictions = [pred["text"] for pred in predictions]

    wer_evaluator = evaluate.load("wer")

    wer = wer_evaluator.compute(predictions=predictions,  references=dataset["transcription"])
    wer

    output_dir.mkdir(exist_ok=True)
    with open(output_dir / "metadata.json", "w") as out_file:
        json.dump({
            "model_id": model_id,
            "dataset_id": dataset_id,
            "dataset_config_name": dataset_config_name,
            "dataset_split": dataset_split,
        }, out_file)
    with open(output_dir / "predictions.json", "w") as out_file:
        json.dump({
            "predictions": predictions,
            "reference": dataset["transcription"]
        }, out_file)

    with open(output_dir  / "metrics.json", "w") as out_file:
        json.dump({
            "wer": wer,
        }, out_file)

if __name__ == "__main__":
    model_id = sys.argv[1]
    dataset_id = sys.argv[2]
    dataset_config_name = sys.argv[3]
    dataset_split = sys.argv[4]

    main(model_id, dataset_id, dataset_config_name, dataset_split)