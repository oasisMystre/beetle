import json
from pathlib import Path

from beetle.walk import walk
from beetle.parser import Parser

parser = Parser()
Path("./grammar/migration.json").write_text(
    json.dumps(parser.parse(walk(Path("./courses"))), indent=4),
    "utf-8",
)
