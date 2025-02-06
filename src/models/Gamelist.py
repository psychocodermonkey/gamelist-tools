#! /usr/bin/env python3
"""
  Program: Gamelist class and specifics for having pythonic representations of the gamelist.xml files.
    Name: Andrew Dixon            File: Gamelist.py
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

import xml.dom.minidom as XML
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass(slots=True)
class Game:
  """
  # Game

  ```python
    Game(path: str, name: str)
  ```

  This class contains a field for all possibilites in gamelist.xml files.
  It is intended to be universial accross all implementations to allow for conversion between implementations.

  ## Additional Attributes:

  | Key                   | ES Data Type         | Default value      | Typical Prompt in FE                |
  |:----------------------|:---------------------|:-------------------|:------------------------------------|
  | path                  | MD_STRING            | ""                 | ENTER PATH                          |
  | name                  | MD_STRING            | ""                 | ENTER NAME                          |
  | sortname              | MD_STRING            | ""                 | ENTER SORTNAME                      |
  | collectionsortname    | MD_STRING            | ""                 | ENTER COLLECTIONS SORTNAME          |
  | description           | MD_MULTILINE_STRING  | ""                 | ENTER DESCRIPTION                   |
  | rating                | MD_RATING            | "0.000000"         | ENTER RATING                        |
  | releasedate           | MD_DATE              | "19700101T000000"  | ENTER RELEASE DATE                  |
  | developer             | MD_STRING            | "unknown"          | ENTER DEVELOPER                     |
  | publisher             | MD_STRING            | ""                 | ENTER PUBLISHER                     |
  | players               | MD_STRING            | "unknown"          | ENTER NUMBER OF PLAYERS             |
  | genres                | MD_STRING            | ""                 | ENTER GAME GENRES                   |
  | region                | MD_STRING            | ""                 | ENTER REGION                        |
  | language              | MD_STRING            | ""                 | THIS GAME'S LANGUAGES               |
  | playcount             | MD_INT               | "0"                | ENTER NUMBER OF TIMES PLAYED        |
  | lastplayed            | MD_TIME              | "0"                | ENTER LAST PLAYED DATE              |
  | gametime              | MD_INT               | "0"                | TOTAL PLAY TIME (SECONDS)           |
  | core                  | MD_LIST              | ""                 | CORE                                |
  | emulator              | MD_LIST              | ""                 | EMULATOR                            |
  | altemulator           | MD_ALT_EMULATOR      | ""                 | SELECT ALTERNATIVE EMULATOR         |
  | arcadesystemname      | MD_STRING            | ""                 | THIS GAME'S ARCADE SYSTEM           |
  | controller            | MD_CONTROLLER        | ""                 | SELECT CONTROLLER                   |
  | favorite              | MD_BOOL              | "false"            | ENTER FAVORITE OFF/ON               |
  | completed             | MD_BOOL              | "false"            | ENTER COMPLETED OFF/ON              |
  | hidden                | MD_BOOL              | "false"            | ENTER HIDDEN OFF/ON                 |
  | broken                | MD_BOOL              | "false"            | ENTER BROKEN OFF/ON                 |
  | kidgame               | MD_BOOL              | "false"            | ENTER KIDGAME OFF/ON                |
  | nogamecount           | MD_BOOL              | "false"            | ENTER DON'T COUNT AS GAME OFF/ON    |
  | hidemetadata          | MD_BOOL              | "false"            | ENTER HIDE METADATA OFF/ON          |
  | nomultiscrape         | MD_BOOL              | "false"            | ENTER NO MULTI-SCRAPE OFF/ON        |
  | md5                   | MD_STRING            | ""                 | MD5 CHECKSUM                        |
  | crc32                 | MD_STRING            | ""                 | CRC32 CHECKSUM                      |
  | cheevosid             | MD_INT               | ""                 | CHEEVOS GAME ID                     |
  | cheevoshash           | MD_STRING            | ""                 | CHEEVOS CHECKSUM                    |
  | scraperid             | MD_INT               | ""                 | SCREENSCRAPER GAME ID               |
  | miximage              | MD_PATH              | ""                 | ENTER PATH TO MIX                   |
  | image                 | MD_PATH              | ""                 | ENTER PATH TO IMAGE                 |
  | thumbnail             | MD_PATH              | ""                 | ENTER PATH TO BOX                   |
  | marquee               | MD_PATH              | ""                 | ENTER PATH TO LOGO                  |
  | boxfront              | MD_PATH              | ""                 | ENTER PATH TO ALT BOXART            |
  | boxback               | MD_PATH              | ""                 | ENTER PATH TO BOX BACKGROUND        |
  | box3d                 | MD_PATH              | ""                 | ENTER PATH TO 3D BOX IMAGE          |
  | cartridge             | MD_PATH              | ""                 | ENTER PATH TO CARTRIDGE             |
  | titleshot             | MD_PATH              | ""                 | ENTER PATH TO TITLE SHOT            |
  | manual                | MD_PATH              | ""                 | ENTER PATH TO MANUAL                |
  | video                 | MD_PATH              | ""                 | ENTER PATH TO VIDEO                 |
  | gamemap               | MD_PATH              | ""                 | ENTER PATH TO MAP                   |
  | bezel                 | MD_PATH              | ""                 | ENTER PATH TO BEZEL (16:9)          |
  | fanart                | MD_PATH              | ""                 | ENTER PATH TO FANART                |
  | magazine              | MD_PATH              | ""                 | ENTER PATH TO MAGAZINE              |
  | folderlink            | MD_FOLDER_LINK       | ""                 | SELECT FOLDER LINK                  |

  """

  # TODO: Add __str__ and __repr__ methods for Game model

  path: str
  name: str
  sortname: Optional[str] = None
  collectionSortName: Optional[str] = None
  description: Optional[str] = None
  rating: Optional[float] = field(default=0)
  releasedate: Optional[str] = field(default_factory=lambda: datetime(1970, 1, 1).isoformat())
  developer: Optional[str] = field(default='unknown')
  publisher: Optional[str] = field(default='unknown')
  players: Optional[str] = field(default='unknown')
  genres: Optional[List[str]] = None
  region: Optional[str] = None
  language: Optional[str] = None
  playcount: Optional[int] = field(default=0)
  lastplayed: Optional[str] = field(default='0')
  gametime: Optional[int] = None
  core: Optional[str] = None
  emulator: Optional[str] = None
  altemulator: Optional[str] = None
  arcadesystemname: Optional[str] = None
  controller: Optional[str] = None
  favorite: Optional[bool] = field(default=False)
  completed: Optional[bool] = field(default=False)
  hidden: Optional[bool] = field(default=False)
  broken: Optional[bool] = field(default=False)
  kidgame: Optional[bool] = field(default=False)
  nogamecount: Optional[bool] = field(default=False)
  hidemetadata: Optional[bool] = field(default=False)
  nomultiscrape: Optional[bool] = field(default=False)
  md5: Optional[str] = None
  crc32: Optional[str] = None
  cheevosid: Optional[str] = None
  cheevoshash: Optional[str] = None
  scraperid: Optional[int] = None
  miximage: Optional[str] = None
  image: Optional[str] = None
  thumbnail: Optional[str] = None
  marquee: Optional[str] = None
  boxfront: Optional[str] = None
  boxback: Optional[str] = None
  box3d: Optional[str] = None
  cartridge: Optional[str] = None
  titleshot: Optional[str] = None
  manual: Optional[str] = None
  video: Optional[str] = None
  gamemap: Optional[str] = None
  bezel: Optional[str] = None
  fanart: Optional[str] = None
  magazine: Optional[str] = None
  folderlink: Optional[str] = None


@dataclass(slots=True)
class Gamelist:
  """
  # Gamelist

  ```python
    Gamelist(path: str, system: str, games: List[Game])
  ```

  ## Properties
  | Property        | Type                | Description |
  |:----------------|:--------------------|:--------------------------------------------------------------------------------------|
  | path            | str                 | The path to the gamelist file.                                                        |
  | system          | str                 | Best guess as to the system based on the enclosing directory name.                    |
  | games           | List[Game]          | A list of games in the gamelist.xml file as Game Objects.                             |
  | xml_decl        | Optional[str]       | The XML declaration at the top of the gamelist file.                                  |
  | altemulator     | Optional[str]       | For forks that utilize the gamelist.xml to store what emulator to launch games with.  |

  """

  # TODO: Add __str__ and __repr__ methods for Gamelist model

  path: str
  system: str
  xml_decl: Optional[str] = field(default='<?xml version="1.0"?>')
  altemulator: Optional[str] = field(default=None)
  games: List[Game] = field(default_factory=list)


@dataclass(slots=True)
class RawGamelist:
  """
  # RawGamelist
  ```python
    RawGameList(path: str, system: Optional[str], xml_decl: Optional[str], gamelist: Optional[XML.Element])
  ```
  This class is used to hold the raw data from a gamelist file, including its path and system name.

  ## Properties
  path     :: str - The path to the gamelist file.
  system   :: Optional[str] - Best guess as to the system based on the enclosing directory name.
  xml_decl :: Optional[str] - The XML declaration at the top of the gamelist file.
  gamelist :: Optional[xml.dom.minidom.Element] - The parsed XML data from the gamelist file.

  ## Properties
  | Property        | Type                | Description |
  |:----------------|:--------------------------------------|:-----------------------------------------------------------------------|
  | path            | str                                   | The path to the gamelist file.                                         |
  | system          | str                                   | Best guess as to the system based on the enclosing directory name.     |
  | xml_decl        | Optional[str]                         | The XML declaration at the top of the gamelist file.                   |
  | gamelist        | Optional[xml.dom.minidom.Element]     | A list of games in the gamelist.xml file as Game Objects.              |

  """

  # TODO: Add __str__ and __repr__ methods for RawGameList model

  path: str
  system: Optional[str] = None
  xml_decl: Optional[str] = field(default='<?xml version="1.0"?>')
  gamelist: Optional[XML.Element] = None
