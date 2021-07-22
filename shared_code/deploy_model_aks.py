import os
import re
import argparse
import yaml

import azureml.core
from azureml.core import Workspace, Experiment, RunConfiguration, Environment
from azureml.core.compute import AksCompute, ComputeTarget
from azureml.core.webservice import Webservice, AksWebservice
from azureml.core.model import Model
from azureml.core.model import InferenceConfig

print("Azure ML SDK version:", azureml.core.VERSION)

parser = argparse.ArgumentParser("Deploy Model to AKS")
parser.add_argument("-f", type=str, help="Controller Config YAML file")
args = parser.parse_args()

with open(args.f, "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    config = config['variables']
print(config)

print('Connecting to workspace')
ws = Workspace.from_config()
print(f'WS name: {ws.name}\nRegion: {ws.location}\nSubscription id: {ws.subscription_id}\nResource group: {ws.resource_group}')

env = Environment.get(workspace=ws, name=config['environment_name'])
model = Model(ws, config['model_name'])

aks_target = ComputeTarget(workspace=ws, name=config['aks_target'])

inf_config = InferenceConfig(entry_script=config['score_script'],
                             source_directory='code/src/',
                             environment=env)
aks_config = AksWebservice.deploy_configuration(token_auth_enabled=False,
                                                auth_enabled=True,
                                                enable_app_insights=True)

aks_service = Model.deploy(workspace=ws,
                           name=config['deployment_name'],
                           models=[model],
                           inference_config=inf_config,
                           deployment_config=aks_config,
                           deployment_target=aks_target,
                           overwrite=True)

aks_service.wait_for_deployment(show_output = True)
print(aks_service.state)