# AutoSaveNewFiles Plugin for Sublime Text

This Sublime Text plugin automatically saves new files to a specified directory with a timestamp-based 
filename and optionally inserts the timestamp as the first line in the file.

## Features

- Automatically saves new files to a configurable directory (default: `~/scratch`).
- Generates filenames based on a configurable format, including customizable timestamps.
- Optionally inserts the timestamp as the first line of the file.
- Handles filename conflicts by appending a counter.

## Installation

1. Open Sublime Text.
2. Go to `Preferences` > `Browse Packages…`.
3. Open the `User` directory.
4. Save the plugin code into a file named `auto_save_new_files.py` in the `User` directory.
5. Create a new file named `AutoSaveNewFiles.sublime-settings` in the same directory with the following content:

```json
{
    "save_directory": "~/working/scratch",
    "filename_format": "{timestamp}.txt",
    "insert_timestamp": true,
    "timestamp_format": "%Y_%m_%d_%H%M%S_%f"
}
