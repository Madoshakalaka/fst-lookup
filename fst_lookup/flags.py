#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright 2019 Eddie Antonio Santos <easantos@ualberta.ca>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Defines the flag diacritics base class, as well as all subclasses.
"""

from typing import Dict

from .symbol import Symbol

__all__ = ['FlagDiacritic', 'Clear', 'Disallow', 'Positive']


class FlagDiacritic(Symbol):
    """
    Base class for all flag diacritics
    """

    __slots__ = 'feature',

    opcode = '!!INVALID!!'

    def __init__(self, feature: str) -> None:
        self.feature = feature

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        else:
            return self.feature == other.feature

    def __hash__(self) -> int:
        return hash((self.opcode, self.feature))

    def __repr__(self) -> str:
        return '{:s}({!r})'.format(type(self).__name__, self.feature)

    def __str__(self) -> str:
        return '@{}.{}@'.format(self.opcode, self.feature)

    def test(self, flags: Dict[str, str]) -> bool:
        """
        Test the flag against the current values.
        """
        raise NotImplementedError

    def apply(self, flags: Dict[str, str]) -> None:
        """
        Destructivley modifies the flags in some way.
        """

    def accepts(self, other):
        raise NotImplementedError('Use .test() instead')


class FlagDiacriticWithValue(FlagDiacritic):
    __slots__ = 'value',

    def __init__(self, feature: str, value: str = None) -> None:
        super().__init__(feature)
        if value is not None:
            self.value = value

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.value == other.value

    def __hash__(self) -> int:
        return hash((self.opcode, self.feature, self.value))

    def __repr__(self) -> str:
        return '{:s}({!r}, {!r})'.format(type(self).__name__,
                                         self.feature, self.value)

    def __str__(self) -> str:
        return '@{}.{}.{}@'.format(self.opcode, self.feature, self.value)


class Clear(FlagDiacritic):
    opcode = 'C'

    def test(self, flags: Dict[str, str]) -> bool:
        """
        Unconditionally accept!
        """
        return True

    def apply(self, flags: Dict[str, str]):
        flags.pop(self.feature, None)


class Disallow(FlagDiacritic):
    opcode = 'D'

    def test(self, flags: Dict[str, str]):
        return self.feature not in flags


class Positive(FlagDiacriticWithValue):
    opcode = 'P'

    def test(self, flags: Dict[str, str]) -> bool:
        return True

    def apply(self, flags: Dict[str, str]) -> None:
        flags[self.feature] = self.value