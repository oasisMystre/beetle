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
"""

from copy import copy
from pathlib import Path

from beetle.utils import find_by, is_object


class Transform:
    """
    Transform parsed data into migration format
    """

    def __init__(self):
        pass

    def concat(self, old: dict, new: dict):
        """
        concat two dicts,
        old key as high priority than new when found in new dict,
        new key has high priority when not found in old dict,
        new value has high priority when not equal to old value.
        """
        mutated = []
        result = copy(old)

        for key, value in old.items():
            if key in new and value != new[key] and not is_object(value):
                result[key] = new[key]
                mutated.append(key)

        for key, value in new.items():
            if key not in old and not is_object(value):
                result[key] = new[key]

        return mutated, result

    def transform(
        self,
        old_node: dict,
        new_node: dict,
    ):
        """
        transform old migration and new input into new output
        """
        old_children = old_node.get("children", [])
        new_children = new_node.get("children", [])
        updates = []
        additions = []
        deletions = []

        for index, child in enumerate(new_children):
            old_child = find_by(old_children, child, "id")

            if not old_child:
                value = copy(child)
                value["index"] = index

                additions.append(value)

            if old_child:
                mutated, value = self.concat(old_child, child)
                value["index"] = index

                if len(mutated) > 0:
                    value["updateKeys"] = mutated
                    updates.append(value)

                if "children" in child:
                    self.transform(old_child, child)

        # new node children has higher priority
        # when an item from old not found in new node then it is deleted from old node
        for index, child in enumerate(old_children):
            new_child = find_by(new_children, child, "id")

            if not new_child:
                # sure this makes removing child when migrating easier
                deletions.append(child)

            # if new_child and "children" in child:
            #     self.transform(old_child, child)

        old_node["deletes"] = deletions
        old_node["updates"] = updates
        old_node["additions"] = additions

        return old_node
