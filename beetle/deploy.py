import random
from beetle.generics import Deploy


class Deployer(Deploy):
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


