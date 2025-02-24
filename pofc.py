#! /usr/bin/env python3
"""
 Program: Proof of concept to walk the directory path, grab the gamelist.xml files and spit them out.
    Name: Andrew Dixon            File: pofc.py
    Date: 9 Jan 2025
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

import argparse
import time
from gamelist_tools import ESDE
from gamelist_tools import Batocera
from gamelist_tools.utils.Ubiquitous import gen_xml


PATH = ''
TEST = ''

def main(path: str) -> None:
  """
  Main
  """
  global TEST

  start_time = time.perf_counter()
  print('Starting gamelist processing...')
  TEST = ESDE.parse_gamelist_data(path)
  end_time = time.perf_counter()

  TEST = sorted(TEST)

  for sys in TEST:
    print(f'------ {sys.system} - # Games: {len(sys.games)} ------')


  print(f"Gamelist file processing time: {end_time - start_time} seconds\n")

  gl = TEST[9]
  gl.sort()
  print(f"XML Generation: for {gl.system}\n")
  Batocera_mapping = Batocera.return_mapping()

  doc = gen_xml(gl, Batocera_mapping)
  xml_str = doc
  print(xml_str)


# If the pofc.py is run (instead of imported as a module),
# call the main() function:
if __name__ == '__main__':
  # Setup the arg parser to import and parse arguments.
  parser = argparse.ArgumentParser()

  parser.add_argument(
    '--path',
    '-p',
    default='__exclude/data/RoamData/ES-DE',
    required=False,
    help='Specify the path to the ES-DE directory.',
  )

  args = parser.parse_args()
  PATH = args.path

  # Register the function to execute on ending the script
  main(PATH)
