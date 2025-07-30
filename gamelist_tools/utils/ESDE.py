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

import os
import re
import xml.dom.minidom as XML
from gamelist_tools.models.Gamelist import Gamelist, Game
from gamelist_tools.utils.Ubiquitous import find_lists, find_files, enclosing_directory, get_text
from gamelist_tools.utils.Ubiquitous import get_gamelist_data, parse_value


# TODO: Methods specific to bringing in and interpreting ES-DE gamelist data.

def return_mapping(invert: bool = False) -> dict:
  """
    # Return Property mapping dictionary
    Map Gamelist object property to XML tag for ES-DE

  ```python
  return_mapping(invert: bool = False) -> dict
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

  # ELEMENT_MAPPING is a dictionary of Game object properties to their corresponding XML node names.
  ELEMENT_MAPPING = {
    'path': 'path',
    'name': 'name',
    'sortname': 'sortname',
    'collectionSortName': 'collectionsortname',
    'description': 'desc',
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
  return ELEMENT_MAPPING if not invert else {value: key for key, value in ELEMENT_MAPPING.items()}


def parse_gamelist_data(esde_path: str) -> list[Gamelist]:
  """
  # Process all gamelist files for ES-DE

  Process all gamelist files in user directory for ES-DE. Searches for es_settings.xml file to
  fetch what the configured downloaded_media directory is in order to populate the path to the
  scraped media. the ```gamelist.xml``` files are stored in a default location within the ES-DE
  directory, so no direct path is taken to point this at a specific directory.

  ## Properties

  | Property        | Type      | Description |
  |:----------------|:----------|:-------------------------------------------|
  | path            | str       | The path to the ES-DE user directory.      |

  """

  settings = get_settings(esde_path)
  media_directory = settings['MediaDirectory'] if settings['MediaDirectory'] else os.path.join(esde_path, 'downloaded_media')
  gamelist_directory = os.path.join(esde_path, 'gamelists')

  imported_data = []
  # Find the gamelists to import information from
  game_lists = find_lists(gamelist_directory)

  # Build a gamelist for each system
  for game_list in game_lists:
    sys = get_system_gamelist(game_list['path'], media_directory)

    imported_data.append(sys)

  return imported_data


def get_settings(path: str) -> dict:
  """
  # Get ES-DE settings from XML file

  Get and process the settings file from the ES-DE user directory.

  ```python
    get_esde_settings(path: str) -> dict:
  ```

  ## Properties

  | Property        | Type     | Description |
  |:----------------|:---------|:------------------------------------------|
  | path            | str      | The path to the ES-DE user directory.     |

  """

  settings_path = os.path.join(path, 'settings', 'es_settings.xml')
  settings = {}
  with open(settings_path, 'r') as f:
    raw_doc = f.read()

    # Find the end of the XML document string so we know where the document actually begins.
    index = 0
    pattern = r"""<\?xml\s+version="(\d+\.\d+|\d*\.\d+)"\s*(?:encoding="[^"]*")?\s*\?>"""
    match = re.match(pattern, raw_doc)
    index = match.end() if match else 0

    # Encapsulate the remainder of the document in a root node so we can access it as children.
    parsed = f"""<root>{raw_doc[index:]}</root>"""
    doc = XML.parseString(parsed)

    # Look for all of the children that have a name and value to be stored in the dictionary.
    for node in doc.getElementsByTagName("*"):
      if node.hasAttribute("name"):
        # settings[node.getAttribute('name')] = node.getAttribute('value')
        name = node.getAttribute('name')
        value = node.getAttribute('value')
        value_type = node.nodeName
        settings[name] = parse_value(value_type, value)

  return settings


def get_system_gamelist(path: str, media_directory: str) -> Gamelist:
  """
  # Build a Gamelist object containing Game objects parsed from a given gamelist.xml file.

  Accepts the path to the gamelist.xml file and the media directory for the system.
  Returns a Gamelist object containing Game objects parsed from the gamelist.xml file.

  ```python
    get_system_gamelist(path: str, media_directory: str) -> Gamelist
  ```

  ## Properties

  | Property        | Type       | Description |
  |:----------------|:-----------|:----------------------------------------------|
  | path            | str        | The path to the ES-DE user directory.         |
  | media_directory | str        | The path to the system's media directory.     |

  """

  # Set up dictionary to map assignment based on media directory.
  set_media_item = {
    # TODO: Need to get a full successful scrape in order to get every possible directory
    '3dboxes': lambda: setattr(game, 'box3d', item),
    'backcovers': lambda: setattr(game, 'boxback', item),
    'covers': lambda: setattr(game, 'boxfront', item),
    'fanart': lambda: setattr(game, 'fanart', item),
    'manuals': lambda: setattr(game, 'manual', item),
    'marquees': lambda: setattr(game, 'marquee', item),
    'miximages': lambda: setattr(game, 'miximage', item),
    'physicalmedia': lambda: setattr(game, 'cartridge', item),
    'screenshots': lambda: setattr(game, 'thumbnail', item),
    'titlescreens': lambda: setattr(game, 'titleshot', item),
    'videos': lambda: setattr(game, 'video', item),
  }

  # Get the raw gamelist data and pre-parse some information from the file.
  raw_sys = get_gamelist_data(path)

  # Initilize gamelist for system
  sys = Gamelist(
    path=raw_sys.path,
    system=raw_sys.system,
    xml_decl=raw_sys.xml_decl
  )

  # Prep the games list for games in the game system object
  sys.games = []

  # Map all the fields from the XML to the field in the Game object
  for raw_game in raw_sys.gamelist.getElementsByTagName('game'):
    game = Game(
      name=get_text(raw_game, 'name'),
      path=get_text(raw_game, 'path'),
      sortname=get_text(raw_game, 'sortname'),
      collectionSortName=get_text(raw_game, 'collectionsortname'),
      description=get_text(raw_game, 'desc'),
      rating=get_text(raw_game, 'rating'),
      releasedate=get_text(raw_game, 'releasedate'),
      developer=get_text(raw_game, 'developer'),
      publisher=get_text(raw_game, 'publisher'),
      genres=str(get_text(raw_game, 'genre')).split(','),
      players=get_text(raw_game, 'players'),
      favorite=get_text(raw_game, 'favorite'),
      completed=get_text(raw_game, 'completed'),
      kidgame=get_text(raw_game, 'kidgame'),
      hidden=get_text(raw_game, 'hidden'),
      broken=get_text(raw_game, 'broken'),
      nogamecount=get_text(raw_game, 'nogamecount'),
      nomultiscrape=get_text(raw_game, 'nomultiscrape'),
      hidemetadata=get_text(raw_game, 'hidemetadata'),
      playcount=get_text(raw_game, 'playcount'),
      controller=get_text(raw_game, 'controller'),
      altemulator=get_text(raw_game, 'altemulator'),
      lastplayed=get_text(raw_game, 'lastplayed'),
    )

    # TODO: Set media file path to be relative gamelist.xml path.
    # Get file name to look in media directory for specific system for scraped media.
    filename = os.path.splitext(os.path.basename(game.path))[0]
    media = find_files(filename, os.path.join(media_directory, sys.system))

    # Populate full media paths for images, etc.
    for item in media:
      set_media_item.get(enclosing_directory(item), lambda: None)()

    # Add the game to the list
    sys.games.append(game)

  return sys
