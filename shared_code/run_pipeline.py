import os
import argparse
import yaml

import azureml.core
from azureml.core import Workspace, Experiment
from azureml.pipeline.core import PublishedPipeline

print("Azure ML SDK version:", azureml.core.VERSION)

parser = argparse.ArgumentParser("Run Pipeline")
parser.add_argument("-f", type=str, help="Pipeline YAML file")
parser.add_argument("-p", type=str, help="Pipeline Id")
args = parser.parse_args()

with open(args.f, "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
print(config)

ws = Workspace.from_config()

pipeline = PublishedPipeline.get(workspace=ws, id=args.p)
pipeline_run = Experiment(ws, config['experiment_name']).submit(pipeline)
print(pipeline_run)
pipeline_run.wait_for_completion()
