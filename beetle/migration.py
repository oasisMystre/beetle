import json
from pathlib import Path

from typing import Dict, List, Optional

from beetle.generics import Deploy


class Migration:
    """
    parse migration
    """

    def __init__(self, file: str, deploy: Deploy):
        self.deploy = deploy
        self.path = Path(file)
        self.migration = self.load(self.path)

    @classmethod
    def load(cls, path: Path) -> dict:
        """
        read migration and load in memory
        """
        return json.loads(path.read_text("utf-8"))

    def migrate(self):
        """
        start migration
        """
        return self._migrate(self.migration)

    def _migrate(self, data: Optional[List[Dict[str, any]]], parent=None, depth=None):
        """
        parse migration data
        """

        if data.get("children") is None:
            return

        children: List[Dict[str, any]] = data["children"]

        updates: Optional[List[Dict[str, any]]] = data.get("updates")
        deletions: Optional[List[Dict[str, any]]] = data.get("deletes")
        additions: Optional[List[Dict[str, any]]] = data.get("additions")

        # addition first before updates
        if additions:
            for addition in additions:
                self.deploy.add(
                    depth=depth,
                    parent=parent,
                    child=data,
                    data=addition,
                )
                children.insert(addition["index"], addition)
                additions.remove(addition)

        if updates:
            # to prevent unwanted behavior while updating indexes
            # we remove from updates after changes have been committed
            indexes = []

            for update in updates:
                self.deploy.update(
                    depth=depth,
                    parent=parent,
                    child=data,
                    data=update,
                )
                children[update["index"]] = update
                indexes.append(update)
                del update["updateKeys"]

            for index in indexes:
                updates.remove(index)

        if deletions:
            indexes = []

            for deletion in deletions:
                self.deploy.delete(
                    depth=depth,
                    parent=parent,
                    child=data,
                    data=deletion,
                )
                # todo check if this has side effect
                # using pop with indexing makes updates un-sync so removing by equal is the best
                children = list(
                    filter(
                        lambda child: child["id"] != deletion["id"],
                        children,
                    )
                )
                indexes.append(deletion)

            for index in indexes:
                deletions.remove(index)

        for child in children:
            self._migrate(child, data, depth + 1)

        self._commit()

    def parse(self):
        """
        parse migration data
        """
        return self._migrate(self.migration, depth=0)

    def _commit(self):
        return self.commit(
            self.path,
            self.migration,
        )

    @classmethod
    def commit(cls, path: Path, migration: dict):
        """
        write migration mutations to disk
        """
        return path.write_text(
            json.dumps(migration, indent=1),
            "utf-8",
        )
