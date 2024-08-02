import sublime
import sublime_plugin
import os
import datetime

# Define a global debug flag
DEBUG = True  # Set to False to turn off debug logging

def debug_log(message):
    if DEBUG:
        print("[AutoSaveNewFiles] " + message)

class AutoSaveNewFilesCommand(sublime_plugin.EventListener):
    def __init__(self):
        self.saved_files = set()
        self.file_timestamps = {}

    def on_new_async(self, view):
        self.save_new_file_with_timestamp(view)

    def on_activated_async(self, view):
        self.save_new_file_with_timestamp(view)

    def on_load_async(self, view):
        self.save_new_file_with_timestamp(view)

    def on_pre_close(self, view):
        self.check_and_delete_empty_file(view)

    def save_new_file_with_timestamp(self, view):
        if view.file_name() in self.saved_files or not view.file_name() is None:
            return

        if not view.is_scratch() and view.file_name() is None and len(view.substr(sublime.Region(0, view.size()))) == 0:
            # Load settings with defaults
            settings = sublime.load_settings("AutoSaveNewFiles.sublime-settings")
            save_directory = os.path.expanduser(settings.get("save_directory", "~/scratch"))
            filename_format = settings.get("filename_format", "{timestamp}.txt")
            insert_timestamp = settings.get("insert_timestamp", True)
            timestamp_format = settings.get("timestamp_format", "%Y_%m_%d_%H%M%S_%f")[:-3]
            debug_log(f"Save directory: {save_directory}")

            # Create the directory if it doesn't exist
            if not os.path.exists(save_directory):
                try:
                    os.makedirs(save_directory)
                    debug_log("Directory created.")
                except Exception as e:
                    debug_log(f"Failed to create directory: {e}")
                    sublime.error_message(f"AutoSaveNewFiles: Failed to create directory {save_directory}")
                    return

            # Generate a timestamp-based filename
            timestamp = datetime.datetime.now().strftime(timestamp_format)
            filename = filename_format.format(timestamp=timestamp)
            debug_log(f"Generated filename: {filename}")

            # Construct the full file path
            file_path = os.path.join(save_directory, filename)
            debug_log(f"Full file path: {file_path}")

            # Check if file already exists
            counter = 1
            while os.path.exists(file_path):
                base, ext = os.path.splitext(filename)
                new_filename = f"{base}_{counter}{ext}"
                file_path = os.path.join(save_directory, new_filename)
                counter += 1

            # Save the new file
            try:
                view.retarget(file_path)
                view.run_command("save")
                debug_log(f"File saved: {file_path}")

                # Insert the timestamp as the first line in the file if enabled
                if insert_timestamp:
                    view.run_command("insert", {"characters": timestamp + "\n"})
                    debug_log(f"Timestamp added to file: {file_path}")
                    view.run_command("save")

                self.saved_files.add(file_path)
                self.file_timestamps[file_path] = timestamp
            except Exception as e:
                debug_log(f"Failed to save file: {e}")
                sublime.error_message(f"AutoSaveNewFiles: Failed to save file {file_path}")

    def check_and_delete_empty_file(self, view):
        file_path = view.file_name()
        if file_path in self.saved_files:
            content = view.substr(sublime.Region(0, view.size())).strip()
            timestamp = self.file_timestamps.get(file_path, "")
            
            if content == timestamp or not content:
                try:
                    os.remove(file_path)
                    debug_log(f"Deleted empty file: {file_path}")
                    self.saved_files.remove(file_path)
                    del self.file_timestamps[file_path]
                except Exception as e:
                    debug_log(f"Failed to delete empty file: {e}")
            else:
                debug_log(f"File not empty, keeping: {file_path}")

# Save this file as auto_save_new_files.py in the Packages/User directory.
