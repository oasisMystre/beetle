import json
from pathlib import Path
from beetle.walk import walk


data = walk(Path("../courses"))

Path("../grammar/walk.json").write_text(json.dumps(data, indent=1),)
