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

# TODO: Write a pofc script to build gamelist from a directory and scan for images in dir to add to image on the list.

import os
import traceback
import argparse
import time
from pathlib import Path
from gamelist_tools import ESDE
# from gamelist_tools import Batocera
from gamelist_tools import EmulationStation
from gamelist_tools.utils.Ubiquitous import gen_xml, output_gamelist


# PATH: str = ''
# OUTPUT: str = ''
GAMELIST_DATA: list = []


def main(path: str, output: str) -> None:
  """
  Main
  """
  global GAMELIST_DATA

  start_time = time.perf_counter()
  print('\n[+] Starting gamelist processing...\n[+] Importing ES-DE game collection data...')
  GAMELIST_DATA = ESDE.parse_gamelist_data(path)
  end_time = time.perf_counter()

  # Sort the gamelists
  GAMELIST_DATA = sorted(GAMELIST_DATA)

  # Process all gamelists and output them to a directory.
  for gl in GAMELIST_DATA:
    try:

      # Sort the games in the gamelist.
      gl.sort()

      # Set relative paths and prefix with a "images" directory.
      gl.set_rel_paths(prepend='images')

      print(f'------ {gl.system} - # Games: {len(gl.games)} ------')

      # Move images around on the object to set what we want showing up for other tags.
      for i, game in enumerate(gl.games):

        if not game.image:
          game.image = game.miximage if game.miximage else game.thumbnail
          # game.image = game.thumbnail if game.thumbnail else game.titleshot

        if not game.thumbnail:
          game.thumbnail = game.boxfront

        # Update the game object after changes are made.
        gl.games[i] = game

      print(f'XML Generation: for {gl.system}\n')
      # Batocera_mapping = Batocera.return_mapping()
      EmulationStation_mapping = EmulationStation.return_mapping(invert=True)

      # doc = gen_xml(gl, Batocera_mapping)
      doc = gen_xml(gl, EmulationStation_mapping)
      # print(xml_str)

      # REGEX to match .chd in gamelist for converting to .m3u on sd cards.
      #  <path>\.\/.*\(Disc 1\)\.chd<\/path>

      # Generate what the output directory needs to be based off system name and generate the gamelist.
      output_dir = Path(f'{output}{gl.system}')
      output_gamelist(doc, output_dir)

    except Exception as e: #noqa E722 Do not use bare except:
      print(f'Error processing :: {gl.system} :: gamelist!')
      print(f"Error Type: {type(e).__name__}")
      print(f"Error Value: {e}")
      print("\n--- Full Traceback ---")
      print(traceback.format_exc())

  print(f'Gamelist file processing time: {end_time - start_time} seconds\n')


# If the pofc.py is run (instead of imported as a module),
# call the main() function:
if __name__ == '__main__':
  # Setup the arg parser to import and parse arguments.
  parser = argparse.ArgumentParser()

  parser.add_argument(
    '--path',
    '-p',
    required=True,
    help='Specify the path to the ES-DE directory.',
  )

  parser.add_argument(
    '--output',
    '-o',
    default='output/',
    required=False,
    help='Specify the output directory for the processed gamelist files.',
  )

  args = parser.parse_args()
  PATH = args.path
  OUTPUT = f'{os.path.normpath(args.output)}/'

  main(PATH, OUTPUT)
