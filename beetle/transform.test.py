import json
from pathlib import Path
from beetle.migration import Migration
from beetle.parser import Parser
from beetle.transform import Transform
from beetle.walk import walk

parser = Parser()
transform = Transform()

old = Migration.load(Path("./grammar/migration.json"))

Path("./grammar/new.json").write_text(
    json.dumps(
        transform.transform(
            old,
            {
                "children": parser.parse(
                    walk(Path("./courses")),
                )
            },
        ),
        indent=1,
    ),
    "utf-8",
)
