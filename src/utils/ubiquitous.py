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
from ..models.Gamelist import RawGamelist


def find_lists(directory: str) -> list:
  """
  Recursively search through the directory structure looking for 'gamelist.xml' files.

  :param directory: The root directory to start searching f rom.
  :return: A list of paths to gamelist.xml files found.

  ```python
    find_lists(directory: str) -> dict:
  ```

  ## Properties
  | Property        | Type                | Description |
  |:----------------|:--------------------|:--------------------------------------------------------------------------------------|
  | directory       | str                 | The path to a directory structure that contains gamelist files.                       |

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
  | Property        | Type                | Description |
  |:----------------|:--------------------|:--------------------------------------------------------------------------------------|
  | path            | str                 | The path to the gamelist file.                                                        |

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


def output(data, path) -> bool:
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
  | Property        | Type                | Description |
  |:----------------|:--------------------|:--------------------------------------------------------------------------------------|
  | value_type      | str                 | Value type defined as the node_name usually.                                          |
  | value           | str                 | Value that is to be converted to a pythonic type.                                     |

  """
  if value_type == 'bool':
    return value.lower() == 'true'  # Convert "true"/"false" to Python bool

  elif value_type == 'int':
    return int(value)  # Convert to integer

  elif value_type == 'string':
    return value  # Keep as string

  return value  # Default to string if type is unknown


def get_text(node, tag):
  """Helper function to get text content of an XML tag."""
  # TODO: Write proper docstring for get_text
  tag_node = node.getElementsByTagName(tag)
  return tag_node[0].firstChild.nodeValue.strip() if tag_node and tag_node[0].firstChild else None


def find_files(name, path):
  """Helper function to crawl directory structure and get files associated with a given filename."""
  # TODO: Write proper docstring for find_files
  return [f for f in Path(path).rglob(name + '*') if f.is_file()]


def enclosing_directory(path: str):
  """Helper function to get the immediate enclosing directory of a file or directory."""
  # TODO: Write proper docstring for enclosing_directory
  return os.path.basename(os.path.dirname(path))