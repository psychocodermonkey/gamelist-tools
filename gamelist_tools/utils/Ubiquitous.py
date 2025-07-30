#! /usr/bin/env python3
"""
 Program: Tools to handle the gamelist.xml files.
    Name: Andrew Dixon            File: ubiquitous.py
    Date: 10 Jan 2025
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
from pathlib import Path
from ..models.Gamelist import RawGamelist, Gamelist, Game


def find_lists(directory: str) -> list:
  """
  Recursively search through the directory structure looking for 'gamelist.xml' files.

  :param directory: The root directory to start searching f rom.
  :return: A list of paths to gamelist.xml files found.

  ```python
    find_lists(directory: str) -> dict:
  ```

  ## Properties

  | Property        | Type      | Description |
  |:----------------|:----------|:---------------------------------------------------------------------|
  | directory       | str       | The path to a directory structure that contains gamelist files.      |

  """

  gamelist_files = []

  # Walk through the directory structure
  for root, _, files in os.walk(directory):
    for file in files:

      # Look for gamelist.xml files
      if file == 'gamelist.xml':

        # Build a dictionary with the system name (folder) ad the full file path
        filepath = os.path.join(root, file)
        gamelist = {
          'system': os.path.basename(root),
          'path': filepath,
        }
        gamelist_files.append(gamelist)

  return gamelist_files


def get_gamelist_data(path: str) -> RawGamelist:
  """
  # Get Gamelist Data
  ```python
    Gamelist.get_gamelist_data(path: str) -> RawGamelist
  ```

  Reads the gamelist file and returns a RawGamelist object containing the path, system, and XML gamelist data as
  a ```xml.dom.minidom.Element```.


  ## Properties

  | Property        | Type      | Description |
  |:----------------|:----------|:------------------------------------|
  | path            | str       | The path to the gamelist file.      |

  """

  raw = RawGamelist(path=path)

  # Dump the raw data from the file.
  with open(path, 'r') as f:
    raw.gamelist = f.read()

    # Find the XML declaration at the head of the file so it doesn't have to be found later.
    index = 0
    pattern = r"""<\?xml\s+version="(\d+\.\d+|\d*\.\d+)"\s*(?:encoding="[^"]*")?\s*\?>"""
    match = re.match(pattern, raw.gamelist)
    if match:
      raw.xml_decl = match.group(0)
      index = match.end()

    # Get the best guess at the system name since most of the time the gamelist.xml is in a "system" directory.
    parts = raw.path.split(os.sep)
    raw.system = parts[next((i for i, x in enumerate(parts) if x == 'gamelist.xml'), None) - 1]

    # Parse and fix the XML for compatibility with XML and set it back to normal XML.
    parsed = f"""<root>{raw.gamelist[index:]}</root>"""
    xml_parser = XML.parseString(parsed)
    root = xml_parser.documentElement
    raw.gamelist = root.getElementsByTagName('gameList')[0]

  return raw


def output(path: str, doc: str) -> None:
  """
  Output the gamelist.xml file in XML format with proper indentation and encoding for all frontends.

  TODO: Write proper docstring for output
  """

  pass


def parse_value(value_type: str, value: str) -> (bool | int | str):
  """
  # Convert XML string values to appropriate Python types.

    ```python
      parse_value(value_type: str, value)
    ```

  ## Properties

  | Property        | Type      | Description |
  |:----------------|:----------|:-------------------------------------------------------|
  | value_type      | str       | Value type defined as the node_name usually.           |
  | value           | str       | Value that is to be converted to a pythonic type.      |

  """

  if value_type == 'bool':
    return value.lower() == 'true'  # Convert "true"/"false" to Python bool

  elif value_type == 'int':
    return int(value)  # Convert to integer

  elif value_type == 'string':
    return value  # Keep as string

  return value  # Default to string if type is unknown


def get_text(node: XML.Element, value: str) -> str:
  """
  # Get text from XML Node

  Return the value for a given XML node name.

  ```python
    get_text(node: xml.dom.minidom.Element, tag: str) - str
  ```

  ## Properties

  | Property        | Type                        | Description |
  |:----------------|:----------------------------|:-------------------------------------------------------------------------|
  | node            | xml.dom.minidom.Element     | XML element to grab the first child that matches the requested tag       |
  | value           | str                         | Element to search for to return the associated value.                    |

  """

  tag_node = node.getElementsByTagName(value)
  return tag_node[0].firstChild.nodeValue.strip() if tag_node and tag_node[0].firstChild else None


def find_files(name: str, path: str) -> list[str]:
  """
  # Find files matching by name in path recursively

  Find all files in a tree that match a file name. Filename is wild carded from beginning of filename.

  ```python
    find_files(name: str, path: str) -> list[str]
  ```

  ## Properties

  | Property        | Type      | Description |
  |:----------------|:----------|:--------------------------------------------|
  | name            | str       | Filename to search directory tree for.      |
  | path            | str       | Starting directory.                         |

  """

  # TODO: Look into if this should or should not be case insensitive.
  # Escape brackets in the string so we can find files with brackets in the name.
  # name = name.replace('[', r'[[]').replace(']', r'[]]') + '*'
  matches = [str(f) for f in Path(path).rglob(name + '*') if f.is_file()]

  # If we don't get any matches, then see if the filename exists in the directory tree.
  #   This is less performant than the above check but works if there are characters rglob
  #.  doesn't lke. Only need to do this if we didn't get hits.
  if not matches:
    matches = [str(f) for f in Path(path).rglob('*') if f.is_file() and name in f.name]

  return matches


def enclosing_directory(path: str):
  """
  # Return Enclosing directory for a file system object.

  File system object can be a direcotry or file, so long as it can be pointed to with a filesystem path.

  ```python
    enclosing_directory(path: str) -> str
  ```

  ## Properties

  | Property        | Type      | Description |
  |:----------------|:----------|:----------------------------------------------------------------|
  | path            | str       | Path to filesystem object to find enclosing directory for.      |

  """

  return os.path.basename(os.path.dirname(path))


def get_rel_path(path: str, depth: int) -> str:
  """
  # Get relative path

  Return a path variable to aid in building relative paths based off of full path variables.

  ```python
    get_rel_path(path, depth) -> str
  ```

  ## Properties

  | Property        | Type      | Description |
  |:----------------|:----------|:----------------------------------------------------------------|
  | path            | str       | Path to filesystem object to return the ending pieces.          |
  | depth.          | int       | How far up the path to traverse before stopping.                |

  """
  # Create a Path object from the string
  path_object = Path(path)

  # Get the parts of the path
  if depth > len(path_object.parts):
      return str(path_object)
  else:
      parts = list(path_object.parts)[-depth:]
      return os.sep.join(parts)


def gen_xml(gamelist: Gamelist, mapping: dict, rootElement: str = 'gameList') -> str:
  """
  # Generate XML

  Generate the XML document string for the Gamelist object using a mapping dictionary for tag names.

  ```python
    gen_xml(gamelist, mapping) -> str
  ```

  ## Properties

  | Property        | Type      | Description |
  |:----------------|:----------|:----------------------------------------------------------------|
  | gamelist        | Gamelist  | Gamelist object that holds all the data for the gameList.xml.   |
  | mapping         | dict      | Dictionary containing object -> XML tag mapping (inverted map)  |

  TODO: Need to handle a way to control what the name of the root element is. This appears to be case sensitive.

  """
  # Create the gamelist root node.
  doc = XML.Document()
  # root = doc.createElement('gameList')
  root = doc.createElement(rootElement)
  doc.appendChild(root)

  # Process all games in the gamelist.
  for game in gamelist.games:
    # Create the "game" child node under the gamelist.
    child = doc.createElement('game')

    # Go thorugh the mappoing dictionary passed to know what and how to populate the children.
    for attr, tag in mapping.items():
      value = getattr(game, attr, None)

      # Only need to build the element/node if there is actually a value.
      if value is not None:
        # Convert lists to string
        if isinstance(value, list):
          value = ', '.join(value)

        # Build the child text node and append to the element
        child_element = doc.createElement(tag)
        child_element.appendChild(doc.createTextNode(str(value)))
        child.appendChild(child_element)

    root.appendChild(child)

  # Pass back the pretty XML document string.
  return doc.toprettyxml(indent='\t', newl='\n')


def gen_dir_gamelist(path: str, extension: str = None) -> Gamelist:
  """
  # Generate Gamelist for games in directory

  Generate XML Gamelist for directory. Filter by extension if needed. Useful if scraping a directory
  for games to then populate media or metadata to output a gamelist.xml.

  ```python
    gen_dir_gamelist(path, ext) -> Gamelist
  ```

  ## Properties

  | Property        | Type      | Description |
  |:----------------|:----------|:----------------------------------------------------------------|
  | path            | str       | String path to directory to to build gamelist off of.           |
  | extension       | str       | File extension to limit build to.                               |

  """
  game_folder = Path(path)

  gamelist = Gamelist(
    path=path,
    system=get_rel_path(path, 1),
    xml_decl='<?xml version="1.0"?>'
  )

  # Process files in directory and build games from them for the gamelist.
  for file in game_folder.iterdir():
    if file.is_file() and (extension is None or file.suffix == extension):
      game = Game(
        # TODO: Modify how we generate the name and drop articles in brackets and parentheses at the end of the name.
        name=os.path.splitext(os.path.basename(file))[0],
        path=f'./{get_rel_path(file, 1)}'
      )

      gamelist.games.append(game)

  return gamelist
