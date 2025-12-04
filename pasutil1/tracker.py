import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)
    
    def on_modified(self, event):
        
        if not event.is_directory:
            current_path = os.path.abspath(event.src_path)
            target_path = os.path.abspath(self.file_path)
            
            
            if current_path == target_path:
                self.output_change()
    
    def output_change(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()

        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")

def monitor_file(file_path):
    if not os.path.exists(file_path):
        print(f"ВНИМАНИЕ: Файл '{file_path}' не существует!")
        return
    
    event_handler = FileChangeHandler(file_path)
    observer = Observer()
    directory = os.path.dirname(file_path) or '.'
    observer.schedule(event_handler, path=directory, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    FILE_TO_WATCH = "C:\\Users\\User\\Desktop\\All\\Programming\\PASUTIL\\pasutil1\\jsons\\saves.json"
    monitor_file(FILE_TO_WATCH)