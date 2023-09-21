# Beetle

Beetle is a filesystem CMS tool. Beetle allows syncing and backup of content using github, cloud storage and more.

## Beetle use case?

Beetle is used on `BeeLearn app` Our creators can keep there content off our database, as well still be able to get content to our database. They don't have to worry about data loss, migrating course to another platform `This is experimental` and having internet access before content can be created, deleted, modified locally.

~~Beetle also allows open source collaborative contribution to it's content. (This feature is built on top of git using middleware listener)~~ [Experimental]

- [ ] Collaborative cms
- [x] Migration is extendable
- [x] Write your own deploy script
- [x] Use your favorite text editor incase of markdown contents
- [ ] Automatic sync between file systems? (Still pending)
- [ ] Migration can be automated using git actions

## Cli Usage

To use beetle you have to install  `python3.10` on your machine

### Create new migration

Scan your cms directory and create a new migration file

```shell
beetle migration:create --path=./courses --output=./migrations/migration.json
```

> --output option is optional default to the root directory command is called with file name `migration.json`

### Update migration

When cms folder is modified or content is modified you can re-scan cms directory

> ~~Beetle is smart to ignore subdirectory that haven't been modified~~ (Still in progress)

```shell
beetle migration:update --file=./migrations/migration.json
```

> --file defaults to same as create, failed when no migration file is found

## Deploy migration

Sync content with database or cloud storage

```shell
beetle migration:deploy --module=./scripts/deployment.py --file=./migration.json  
```

```py
#deployment.py
from beetle.deploy import Deploy

# Example deployer using beelearn database sync for explanation
class Deployer(Deploy):
    def update(self, depth, data):
        pass 

    def add(self, depth, data):
        # depth is based on sub directories 
        # if depth is not corelate with how your data is structured use recursion or implement your own logic
        match depth:
            case 0:
                course = {
                    "name": parseName(data["name"]),
                    "isVisible": False,
                }     

                course = Course.objects.create(**course)

                modules = data.get("children", [])

                for module in modules:
                    module_data = {
                        "course": course.pk,
                        "name": parseName(data["name"]),
                        "isVisible": True
                    }

                    module = Module.objects.create(**module_data)

                    lessons = module.get("children", [])

                    for lesson in lessons:
                        lesson = Lesson.objects.create(**lesson_data)
            
            case 1:
                ...
            case 2:
                ...
            case 3:
                ...       
                

    def delete(self, depth, data):
        match depth:
            case 0:
                Course.objects.delete(pk=data["databaseId"])
            case 1:
                ...
            case 2:
                ...
            case 3:
                ...
```

## Format

Add numbering to front of your file or folder name if you care about how your cms is structured

Change in file or folder position trigger the index change update, you can ignore using a conditional statement in deploy script

```py
...
def update(self, depth, data, **kwargs):
    if "index" in data["updateKeys"]:
        return
```

> updateKeys contain list of mutated keys e.g path, name, index e.t.c

## How Beetle works

First we recurse through cms folder using as nested list to structure our result

```py
"""
courses/
    0.Python/
        0.Introduction/
            0.Introduction To Python/
                0.Python.md
                1.Python Creator.md
"""

# outputs 

(
    [
        courses,
        (
            0.Introduction,
            (
                0.Introduction To Python,
                (
                    0.Python.md,
                    1.Python Creator.md
                )
            )
        )
    ]
)
```

Then the result is pass on to our parser which structure it in form of beetle migration file schema.

This is also recursive

```py
{
    "children": [
        {
            "id": file.sys_uno,
            "path": file.path,
            "name": file.name,
            children: [...]
        }
    ],
}
```

This pipe through a transformer to diff old migration and new migration file to get updates, additions and deletes.

Same, also recursive

```py
{
    "children": [...
    ],
    "updates": [],
    "additions": [],
    "deletes": [],
}
```

Then migration occurs, the deployment script works on the updates, additions and deletes syncing with database or cloud storage

```py
migration = Migration("../migration.json", Deployer())
migration.migrate()
```

## Contribution and roadmap

1. We want to make algorithm faster and more efficient
2. Make beetle work across multiple file system
3. Utilize github to prevent migration clash across multiple contributors
4. Ignore scanning whole folder if last modified is equal to last time migration depth is modified

## Usage

Beetle is currently used on BeeLearn app for open source cms contributions and more

<img
    src="https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/545/647/datas/original.png"
    alt="BeeLearn"
    width="96"
    height="96"
    style="border-radius: 100px;" />

## Buy me coffee

To support me and more open source projects like this,

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/lyonkvalid)