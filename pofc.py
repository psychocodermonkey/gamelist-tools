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

# import traceback
import argparse
import time
from gamelist_tools import ESDE

# from gamelist_tools import Batocera
from gamelist_tools import EmulationStation
from gamelist_tools.utils.Ubiquitous import gen_xml, get_rel_path


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

  print(f'Gamelist file processing time: {end_time - start_time} seconds\n')

  # gl = TEST[0]
  for gl in TEST:
    try:
      gl.sort()

      for i, game in enumerate(gl.games):
        game.video = None

        # Update paths for images to relative paths inside the system directory.
        image_tags = [
          'miximage',
          'marquee',
          'boxfront',
          'boxback',
          'box3d',
          'cartridge',
          'titleshot',
          'thumbnail',
          'manual',
          'video',
          'gamemap',
          'bezel',
          'fanart',
          'magazine',
        ]

        for tag in image_tags:
          value = getattr(game, tag)
          if value:
            value = './images/' + get_rel_path(value, 2)
            setattr(game, tag, value)


        if not game.image:
          game.image = game.miximage

        if not game.thumbnail:
          game.thumbnail = game.boxfront

        # Update the game object after changes are made.
        gl.games[i] = game

      print(f'XML Generation: for {gl.system}\n')
      # Batocera_mapping = Batocera.return_mapping()
      EmulationStation_mapping = EmulationStation.return_mapping(invert=True)

      # doc = gen_xml(gl, Batocera_mapping)
      doc = gen_xml(gl, EmulationStation_mapping)
      xml_str = doc
      # print(xml_str)

      # REGEX to match .chd in gamelist for converting to .m3u on sd cards.

      with open('output/' + gl.system + '.xml', 'w') as file:
        file.write(xml_str)

    except:
      # exc_type, exc_value, exc_traceback = sys.exc_info()
      # # Print a generic message
      print(f'{gl.system} error processing gamelist!')

      # # Print the exception type and value
      # print(f"Error Type: {exc_type.__name__}")
      # print(f"Error Value: {exc_value}")

      # # Print the full traceback
      # print("\n--- Full Traceback ---")
      # # traceback.print_exc() # Prints the traceback to stderr by default
      # # Alternatively, to get the traceback as a string:
      # traceback_str = traceback.format_exc()
      # print(traceback_str)


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
