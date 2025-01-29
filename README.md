# Gamelist-tools (for ES-DE)

This is a tool for manipulating and updating the ES-DE gamelist.xml files to include information expected in other EmulationStation frontends. ES-DE utilizes a folder structure for media and thusly is not included in it's gamelist.xml files. This tool will insert the XML tags needed to direct EmulationStation where to find boxart, screenshots, etc... and making copying media to those locations easier.

## File Structure

The script expects a folder structure that looks like this:

- Roms/
  - System Name/
    - downloaded_media/
      - 3dboxes/
      - covers/
      - manuals/
      - marquees/
      - miximages/
      - physicalmedia/
      - screenshots/
      - titlescreens/
      - videos/
    - game.rom
    - gamelist.xml
    ...

Since EmulationStation expects that the media paths are relative to the gamelist.xml this allows thags to be inserted and keep the ES-DE file structure. Not all directories are needed, but included for ease of copying from the ES-DE media directory.

## Documentation from [Batocera-EmulationStation](https://github.com/batocera-linux/batocera-emulationstation/blob/master/GAMELISTS.md)

There are a few types of metadata. This is documented here as what is currently implemented for this tool. See [Batocera-EmulationStation](https://github.com/batocera-linux/batocera-emulationstation/blob/master/GAMELISTS.md) to check if there is updated information. This may not be accurate across all distributions of EmulationStation.

- `string` - just text.
- `image_path` - a path to an image. This path should be either the absolute to the image, a path relative to the system games folder that starts with "./" (e.g. `./mm2_image.png`), or a path relative to the home directory that starts with "~/" (e.g. `~/.emulationstation/downloaded_images/nes/mm2-image.png`).  Images will be automatically resized by OpenGL to fit the corresponding `<image>` tag in the current theme.  Smaller images will load faster, so try to keep resolution low!
- `video_path` - a path to a video. Similar to `image_path`.
- `float` - a floating-point decimal value (written as a string).
- `integer` - an integer value (written as a string).
- `datetime` - a date and, potentially, a time.  These are encoded as an ISO string, in the following format: "%Y%m%dT%H%M%S%F%q".  For example, the release date for Chrono Trigger is encoded as "19950311T000000" (no time specified).

Some metadata is also marked as "statistic" - these are kept track of by ES and do not show up in the metadata editor.  They are shown in certain views (for example, the detailed view shows both `playcount` and `lastplayed`).

### `game` Element metadata

- `name` - string, the displayed name for the game.
- `desc` - string, a description of the game.  Longer descriptions will automatically scroll, so don't worry about size.
- `image` - image_path, the path to an image to display for the game (like box art or a screenshot).
- `thumbnail` - image_path, the path to a smaller image, displayed in image lists like the grid view.  Should be small to ensure quick loading.
- `video` - video_path, the path to a video to display for the game, for themes that support the _video_ viewstyle.
- `rating` - float, the rating for the game, expressed as a floating point number between 0 and 1.  Arbitrary values are fine (ES can display half-stars, quarter-stars, etc).
- `releasedate` - datetime, the date the game was released.  Displayed as date only, time is ignored.
- `developer` - string, the developer for the game.
- `publisher` - string, the publisher for the game.
- `genre` - string, the (primary) genre for the game.
- `players` - integer, the number of players the game supports.
- `playcount` - statistic, integer, the number of times this game has been played.
- `lastplayed` - statistic, datetime, the last date and time this game was played.

### `folders` Element metadata

- `name` - string, the displayed name for the folder.
- `desc` - string, the description for the folder.
- `image` - image_path, the path to an image to display for the folder.
- `thumbnail` - image_path, the path to a smaller image to display for the folder.

## Planned Features

List of currently planned features.

- [ ] Add support for pointing to ES-DE install to find gamelist and media directories.
- [ ] Add support for reading ES-DE config to find `downloaded_media` directory.
- [ ] Add support for selecting what metadata should be added to the `gamelist.xml` files.
- [ ] Add support for exporting to `Roms` directory for output and move data accordingly.
- [ ] Add support for copying media to the appropriate locations based on the updated `gamelist.xml` files.
- [ ] Add support for mapping directory / system names for systems that use different conventions for system folder names.
- [ ] Add support for adding sortname to appropriately sort games that have `The` as the first word.
- [ ] Add support for creating a backup of the original `gamelist.xml` before making changes.
