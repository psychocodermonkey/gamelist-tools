#! /usr/bin/env python3
"""
 Program: Create dummy data for testing purposes.
    Name: Andrew Dixon            File: CreateDummyData.py
    Date: 5 Aug 2025
   Notes: Duplicates XML files so settings and metadata can be parsed and processed.

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
import argparse
import shutil


def main(source_dir, dest_dir) -> None:
  # Normalize and validate source directory
  source_dir = os.path.abspath(source_dir)
  dest_dir = os.path.abspath(dest_dir)

  if not os.path.isdir(source_dir):
    raise NotADirectoryError(f'Source path does not exist or is not a directory: {source_dir}')

  for root, dirs, files in os.walk(source_dir):
    # Construct relative path from the source base
    relative_path = os.path.relpath(root, source_dir)

    # Corresponding path in destination
    dest_path = os.path.join(dest_dir, relative_path)

    # Make sure destination directory exists
    os.makedirs(dest_path, exist_ok=True)

    for file in files:
      source_file = os.path.join(root, file)
      dest_file = os.path.join(dest_path, file)

      # Copy .xml files, create 0-byte for everything else
      if file.lower().endswith('.xml'):
        shutil.copy2(source_file, dest_file)
      else:
        open(dest_file, 'wb').close()


if __name__ == '__main__':
  # Call example is python CreateDummyData.py /path/to/source /path/to/destination
  parser = argparse.ArgumentParser(
    description='Create dummy file structure for testing. Copy XML data files for parsing.'
  )

  parser.add_argument(
    'source',
    help='Source directory to walk.'
    )

  parser.add_argument(
    'destination',
    help='Destination directory for structure and files.'
    )

  args = parser.parse_args()

  main(args.source, args.destination)
  print(f'Dummy structure duplicated at: {args.destination}')
