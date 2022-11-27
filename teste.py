import json

with open("teste_j.json", 'r+') as f:
        data = json.load(f)
        data["instances"].pop(0)
        f.seek(0) 
        json.dump(data,f, indent=4)
        f.truncate()