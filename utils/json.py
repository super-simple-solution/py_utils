import json

def jsonWrite(output_path, data):
  with open(f"{output_path}.json", "w") as f:
    json.dump(data, f, ensure_ascii=False)