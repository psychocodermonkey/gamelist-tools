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
from ..models.Gamelist import Gamelist, Game
from .ubiquitous import find_lists, get_gamelist_data, get_text, parse_value, find_files, enclosing_directory


# TODO: Methods specific to bringing in and interpreting ES-DE gamelist data.
# TODO: Key / Value mapping idea with a dictionary and list comprehension.
#       Each ES type can have it's own mapping into this data object as a dictionary. Then use a list comprehension to create
#         a reversed version for key back.
#       The list comprehension is: inv_data = {value: key for key, value in original_dict.items()}


def parse_gamelist_data(esde_path: str) -> list[Gamelist]:
  """
  # Process all gamelist files for ES-DE

  # TODO: Write proper docstring for parse_gamelist_data
  """

  settings = get_settings(esde_path)
  media_directory = settings['MediaDirectory']
  # game_directory = settings['ROMDirectory']
  gamelist_directory = os.path.join(esde_path, 'gamelists')

  imported_data = []
  # Find the gamelists to import information from
  game_lists = find_lists(gamelist_directory)

  # Set up dictionary to map assignment based on media directory
  set_media_item = {
    # TODO: Need to get a full successful scrape in order to get every possible directory
    '3dboxes': lambda: setattr(game, 'box3d', item),
    'covers': lambda: setattr(game, 'boxfront', item),
    'manuals': lambda: setattr(game, 'manual', item),
    'marquees': lambda: setattr(game, 'marquee', item),
    'miximages': lambda: setattr(game, 'miximage', item),
    'physicalmedia': lambda: setattr(game, 'cartridge', item),
    'screenshots': lambda: setattr(game, 'thumbnail', item),
    'titlescreens': lambda: setattr(game, 'titleshot', item),
    'videos': lambda: setattr(game, 'video', item),
  }

  # Build a gamelist for each system
  for game_list in game_lists:
    raw_sys = get_gamelist_data(game_list['path'])
    # Initilize gamelist for system
    sys = Gamelist(
      path=raw_sys.path,
      system=raw_sys.system,
      xml_decl=raw_sys.xml_decl
    )

    # Prep the games list for games in the game system object
    sys.games = []

    # Map all the fields from the XML to the field in the Game object
    for game in raw_sys.gamelist.getElementsByTagName('game'):
      game = Game(
        name=get_text(game, 'name'),
        path=get_text(game, 'path'),
        sortname=get_text(game, 'sortname'),
        collectionSortName=get_text(game, 'collectionsortname'),
        description=get_text(game, 'desc'),
        rating=get_text(game, 'rating'),
        releasedate=get_text(game, 'releasedate'),
        developer=get_text(game, 'developer'),
        publisher=get_text(game, 'publisher'),
        genres=str(get_text(game, 'genre')).split(','),
        players=get_text(game, 'players'),
        favorite=get_text(game, 'favorite'),
        completed=get_text(game, 'completed'),
        kidgame=get_text(game, 'kidgame'),
        hidden=get_text(game, 'hidden'),
        broken=get_text(game, 'broken'),
        nogamecount=get_text(game, 'nogamecount'),
        nomultiscrape=get_text(game, 'nomultiscrape'),
        hidemetadata=get_text(game, 'hidemetadata'),
        playcount=get_text(game, 'playcount'),
        controller=get_text(game, 'controller'),
        altemulator=get_text(game, 'altemulator'),
        lastplayed=get_text(game, 'lastplayed'),
      )

      # Get file name to look in media directory for specific system for scraped media.
      filename = os.path.splitext(os.path.basename(game.path))[0]
      media = find_files(filename, os.path.join(media_directory, sys.system))

      # Populate full media paths for images, etc.
      for item in media:
        set_media_item.get(enclosing_directory(item), lambda: None)()

      # Add the game to the list
      sys.games.append(game)

    imported_data.append(sys)

  return imported_data


def get_settings(path: str) -> dict:
  """
  # Get ES-DE settings from XML file

  Get settings for ES-DE from the user directory.

  ```python
    get_esde_settings(path: str) -> dict:
  ```

  ## Properties
  | Property        | Type                | Description |
  |:----------------|:--------------------|:--------------------------------------------------------------------------------------|
  | path            | str                 | The path to the ES-DE user directory                                                  |

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
