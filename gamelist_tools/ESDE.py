#! /usr/bin/env python3
"""
 Program: Objects and tools for ES-DE gamelist interpertation.
    Name: Andrew Dixon            File: ESDE.py
    Date: 16 Jan 2025
   Notes:

    Copyright (C) 2025  Andrew Dixon

    This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with this program.
    If not, see <https://www.gnu.org/licenses/>.

........1.........2.........3.........4.........5.........6.........7.........8.........9.........0.........1.........2.........3..
"""


# TODO: Methods specific to bringing in and interpreting ES-DE gamelist data.
# TODO: Key / Value mapping idea with a dictionary and list comprehension.
#       Each ES type can have it's own mapping into this data object as a dictionary. Then use a list comprehension to create a reversed version for key back.
#       The list comprehension is: inv_data = {value: key for key, value in original_dict.items()}
