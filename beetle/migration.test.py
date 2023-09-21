# from pathlib import Path
from pathlib import Path
import random
from beetle.migration import Deploy, Migration


class BeeLearnDeployer(Deploy):
    """
    jj
    """

    def add(self, data: dict, **kwargs):
        data["databaseId"] = random.randint(0, 9999)


    def update(self, data: dict, **kwargs):
        data["databaseId"] = random.randint(0, 9999)

    def delete(self, data: dict, **kwargs):
        pass
        # data["databaseId"] = random.randint(0, 9999)


parser = Migration(Path("./grammar/migration.json"), BeeLearnDeployer())
parser.parse()
# print(parser.migration)
