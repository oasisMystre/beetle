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
            if (
                key in new
                and value != new[key]
                and not isinstance(value, (dict, tuple, list))
            ):
                result[key] = new[key]
                mutated.append(key)

        for key, value in new.items():
            if key not in old and not isinstance(value, (dict, tuple, list)):
                result[key] = new[key]
                mutated.append(key)

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
            old_child = list(
                filter(
                    lambda x: x["id"] == child.get("id"),
                    old_children,
                )
            )
            is_exist = len(old_child) > 0

            if not is_exist:
                value = copy(child)
                value["index"] = index
                additions.append(value)

            if is_exist:
                child["index"] = index

                mutated, value = self.concat(old_child[0], child)

                if len(mutated) > 0:
                    value["updateKeys"] = mutated
                    updates.append(value)

            if len(old_child) > 0 and "children" in child:
                self.transform(old_child[0], child)

        for index, child in enumerate(old_children):
            new_child = list(
                filter(
                    lambda x: x["id"] == child.get("id"),
                    new_children,
                )
            )

            if len(new_child) == 0:
                # sure this makes removing child when migrating easier
                deletions.append(child)

        old_node["deletes"] = deletions
        old_node["updates"] = updates
        old_node["additions"] = additions

        return old_node
