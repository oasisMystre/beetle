"""
MIT License

Copyright (c) 2023 Include caleb.fun

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Beetle cli commands
```shell
beetle migration:create --path=./courses --output=./migrations
beetle migration:update --file=./migrations/migration.json
beetle migration:deploy --file=./migrations/migration.json
```
"""

from pathlib import Path
from typing import Optional

import json
import click


from beetle import Transform, Migration, walk, Parser


def _transform(migration_file: Path, cms_dir: Path):
    """
    get transformed parsed migrations
    """

    transform = Transform()
    parser = Parser()

    return transform.transform(
        Migration.load(migration_file),
        {
            "children": parser.parse(walk(cms_dir)),
        },
    )


SCHEMA = """
{
"input": "%s",
%s
}
"""


@click.group()
def migration():
    """
    Beetle cli commands
    ```shell
    beetle migration:create --path=./courses --output=./migrations
    beetle migration:update --file=./migrations/migration.json
    beetle migration:deploy --file=./migrations/migration.json
    ```
    """


@migration.command("migration:create")
@click.option(
    "--path",
    type=Path,
    help="path where cms content is located",
)
@click.option(
    "--output",
    type=Path,
    default="./migration.json",
    help="folder or file to output migration content",
)
def create(path: Path, output: Optional[Path]):
    """
    create migration file
    """
    if output.exists() and not click.confirm(
        "Already exist, do you want to override?",
    ):
        return

    output.write_text(
        SCHEMA
        % (
            path,
            '"children": []',
        ),
        "utf-8",
    )

    output.write_text(
        json.dumps(_transform(output, path), indent=1),
        "utf-8",
    )

    click.echo(
        "Migration created successfully",
        color="green",
    )


@migration.command("migration:update")
@click.option(
    "--file",
    type=Path,
    default="./migration.json",
    help="Migration file",
)
def update(file: Path):
    """
    update migration when folder content changed
    [file: Optional[str]] migration file
    """

    if not file.exists():
        click.echo(
            "Migration file does not exist",
            color="red",
        )
        return

    data = Migration.load(file)
    cms_dir = Path(data["input"])

    file.write_text(
        json.dumps(_transform(file, cms_dir), indent=1),
        "utf-8",
    )


@migration.command("migration:deploy")
@click.option(
    "--file",
    type=Path,
    default="./migration.json",
    help="Migration file",
)
@click.option(
    "--module",
    type=str,
    help="Deployment script [Has only one class that implements beetle.generics.Deployment]",
)
def deploy(file: Path, module: Optional[str]):
    """
    deploy cms content to cloud or database
    [file: Optional[str]] migration file
    """
    module = __import__(module, fromlist=["Deploy"])
    if not hasattr(module, "Deploy"):
        click.echo("%s don't have a export class `Deploy`")
        return

    klass = getattr(module, "Deployer")
    _migration = Migration(file, klass())
    _migration.migrate()

    click.echo("Migration deployed successfully")


if __name__ == "__main__":
    migration()
