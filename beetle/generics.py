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

Generic abstractions
[Deploy] Abstract class that can be inherited to sync cms content with cloud, database e.t.c   
"""

from abc import ABC, abstractmethod


class Deploy(ABC):
    """
    Sync cms content abstraction
    """

    @abstractmethod
    def update(self, data: dict, *, depth: int, parent: dict, child: dict):
        """
        update entry in database, cloud etc
        """

    @abstractmethod
    def add(self, data: dict, *, depth: int, parent: dict, child: dict):
        """
        add new entry in database, cloud etc
        """

    @abstractmethod
    def delete(self, data: dict, *, depth: int, parent: dict, child: dict):
        """
        delete entry from data, cloud etc
        """
