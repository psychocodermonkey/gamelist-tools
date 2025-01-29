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

from os import walk
from os.path import join, dirname, basename


def find_lists(directory: str) -> dict:
  """
  Recursively search through the directory structure looking for 'gamelist.xml' files.

  :param directory: The root directory to start searching f rom.
  :return: A list of paths to gamelist.xml files found.
  """

  gamelist_files = []

  # Walk through the directory structure
  for root, _, files in walk(directory):
    for file in files:
      if file == 'gamelist.xml':
        filepath = join(root, file)
        gamelist = {
          'system': basename(root),
          'path': filepath,
        }
        gamelist_files.append(gamelist)

  return gamelist_files


def read(path) -> list:
  """
  Read a gamelist.xml file and parse it into a Python dictionary.
  """
  pass


def update(path) -> bool:
  """
  Update the gamelist.xml file at the given path with new data.
  """
  pass


def output(data, path) -> bool:
  """
  Output the parsed data to a gamelist.xml file.
  """
  pass
