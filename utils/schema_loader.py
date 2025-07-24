import json, os

def load_schema(name, folder=os.path.join("schemas")):
    with open(os.path.join(folder, f"{name}.json"), "r") as file:
        return json.load(file)