import os
import argparse
from azureml.core import Workspace, Datastore, Dataset

def parse_args():
    parser = argparse.ArgumentParser(description="Register dataset")
    parser.add_argument("-n", type=str, help="Name of the dataset you want to register")
    parser.add_argument("-d", type=str, help="Description of the dataset you want to register")
    parser.add_argument("-l", type=str, help="local path of the dataset folder", default='code/data/')
    parser.add_argument("-p", type=str, help="Path on data store", default='data/')
    return parser.parse_args()

def main():
    args = parse_args()
    print(args)
    ws = Workspace.from_config()
    datastore = ws.get_default_datastore()
    datastore.upload(src_dir = args.l, target_path = args.p, overwrite = True, show_progress = True)
    print(f"About to register dataset {args.n}")

    dataset = Dataset.File.from_files(path=[(datastore, args.p)], validate=True)
    dataset = dataset.register(workspace=ws,name=args.n, description=args.d)
    print("Dataset registered")

if __name__ == "__main__":
    main()