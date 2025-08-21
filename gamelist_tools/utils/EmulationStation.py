#! /usr/bin/env python3
"""
 Program: Tools for handling Emulation Station Gamelists
    Name: Andrew Dixon            File: EmulationStation.py
    Date: 23 Feb 2025
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

import os
import re
import xml.dom.minidom as XML
from gamelist_tools.models.Gamelist import Gamelist, Game
from gamelist_tools.utils.Ubiquitous import find_lists, find_files, enclosing_directory, get_text
from gamelist_tools.utils.Ubiquitous import get_gamelist_data, parse_value


def return_mapping(invert: bool = False) -> dict:
  """
    # Return Property mapping dictionary

    Map Gamelist object property to XML tag for ES-DE.

    ```python
    eturn_mapping(invert: bool = False) -> dict
    ```

  # Properties

    | Property        | Type      |Value  | Description |
    |:----------------|:----------|:------|:-------------------------------------------|
    | invert          | str       |False  | Element mapping -                          |
    |                 |           |       |   Key:   Object Attribute.                 |
    |                 |           |       |   Value: XML Element value.                |
    | invert          | str       |True   | The path to the ES-DE user directory.      |
    |                 |           |       |   Key:   XML Element value.                |
    |                 |           |       |   Value: Object Attribute.                 |
  """

  ELEMENT_MAPPING = {
    'path': 'path',
    'name': 'name',
    'sortname': 'sortname',
    'collectionSortName': 'collectionsortname',
    'description': 'desc',
    'image': 'image',
    'video': 'video',
    'marquee': 'marquee',
    'thumbnail': 'thumbnail',
    'fanart': 'fanart',
    'titleshot': 'titleshot',
    'manual': 'manual',
    'magazine': 'magazine',
    'gamemap': 'map',
    'rating': 'rating',
    'releasedate': 'releasedate',
    'developer': 'developer',
    'publisher': 'publisher',
    'genres': 'genre',
    'players': 'players',
    'favorite': 'favorite',
    'completed': 'completed',
    'kidgame': 'kidgame',
    'hidden': 'hidden',
    'broken': 'broken',
    'nogamecount': 'nogamecount',
    'nomultiscrape': 'nomultiscrape',
    'hidemetadata': 'hidemetadata',
    'playcount': 'playcount',
    'controller': 'controller',
    'altemulator': 'altemulator',
    'lastplayed': 'lastplayed',
    'folderlink': 'folderlink',
  }

  # Return the ELEMENT_MAPPING dictionary based on the way invert is set.
  return ELEMENT_MAPPING if invert else {value: key for key, value in ELEMENT_MAPPING.items()}
