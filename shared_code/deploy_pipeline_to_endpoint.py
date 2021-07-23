import os
import yaml
import argparse
import azureml.core
from azureml.core import Workspace
from azureml.pipeline.core import Pipeline, PublishedPipeline, PipelineEndpoint

print("Azure ML SDK version:", azureml.core.VERSION)

parser = argparse.ArgumentParser("Publish pipeline to pipeline endpoint")
parser.add_argument("-p", type=str, help="Pipeline ID of pipeline to add")
parser.add_argument("-f", type=str, help="Controller Config YAML file")
args = parser.parse_args()

with open(args.f, "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    config = config['variables']
print(config)

ws = Workspace.from_config()

endpoint_name = config['training_pipeline_name'] + '-endpoint'
pipeline_id = args.p
published_pipeline = PublishedPipeline.get(workspace=ws, id=pipeline_id)

try:
    pl_endpoint = PipelineEndpoint.get(workspace=ws, name=endpoint_name)
    pl_endpoint.add_default(published_pipeline)
    print(f'Added pipeline {pipeline_id} to Pipeline Endpoint with name {endpoint_name}')
except Exception:
    print(f'Will create new Pipeline Endpoint with name {endpoint_name} with pipeline {pipeline_id}')
    pl_endpoint = PipelineEndpoint.publish(workspace=ws,
                                           name=endpoint_name,
                                           pipeline=published_pipeline)
