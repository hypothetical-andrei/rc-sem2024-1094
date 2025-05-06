import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f"Created: {event.src_path}")

    def on_modified(self, event):
        print(f"Modified: {event.src_path}")

    def on_deleted(self, event):
        print(f"Deleted: {event.src_path}")

    def on_moved(self, event):
        print(f"Moved: from {event.src_path} to {event.dest_path}")


if __name__ == "__main__":
    path_to_watch = "C:\\dev\\comp-net\\temp"  # Change this to your folder
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)

    observer.start()
    print(f"Watching {path_to_watch}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
