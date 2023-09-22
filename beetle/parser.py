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

from pathlib import Path
from typing import List, Union, Tuple

from .utils import is_iterable


class Parser:
    """
    A class for parsing directories and generating a hierarchical representation.
    """

    def __init__(self):
        pass

    def parse(
        self,
        directories: List[Union[Path, Tuple[Path, List[Path]]]],
    ):
        """
        Recursively parses directories and generates a hierarchical representation.
        """
        root = []

        for directory in directories:
            if is_iterable(directory):
                parent, children = directory
            else:
                parent, children = directory, []

            node = {
                "id": parent.lstat().st_ino, #todo make this consistence across multiple file system
                "name": parent.name,
                "path": str(parent),
                "children": self.parse(children),
            }

            if len(node["children"]) == 0:
                del node["children"]

            root.append(node)

        return root
