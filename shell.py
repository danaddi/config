import datetime
import os
import subprocess
from vfs import VFS

class Shell:
    def __init__(self, config):
        self.config = config
        self.vfs = VFS(config['vfs_path'])
        self.current_path = '/'
    def execute(self, command):

        parts = command.strip().split()
        if not parts:
            return ''

        cmd = parts[0]
        args = parts[1:]

        if cmd == 'ls':
            return self.ls()
        elif cmd == 'cd':
            return self.cd(args[0]) if args else 'cd: missing argument'
        elif cmd == 'exit':
            return self.exit()
        elif cmd == 'touch':
            return self.touch(args[0]) if args else 'touch: missing file'
        elif cmd == 'rm':
            return self.rm(args[0]) if args else 'rm: missing file'
        else:
            return f"Unknown command: {cmd}"

    def ls(self):
        try:
            contents = self.vfs.list_dir(self.current_path)
            if contents:
                return '\n'.join(contents)
            return 'Empty directory'
        except Exception as e:
            return f"ls: error listing directory: {str(e)}"

    def cd(self, path):
        try:
            if path == '..':  # Переход на уровень выше
                new_path = os.path.dirname(self.current_path.rstrip('/'))
                self.current_path = new_path if new_path else '/'
            else:
                new_path = os.path.join(self.current_path, path).replace('\\', '/')
                if self.vfs.directory_exists(new_path):
                    self.current_path = new_path
                else:
                    return f"cd: no such directory: {path}"
            return f"Current directory {self.current_path}"
        except Exception as e:
            return f"cd: error changing directory: {str(e)}"

    def exit(self):
        self.vfs.close()
        return "Exiting..."

    def touch(self, filename):
        try:
            file_path = os.path.join(self.current_path, filename).replace('\\', '/')
            if self.vfs.file_exists(file_path):
                return f"touch: file already exists: {filename}"
            self.vfs.create_file(file_path)
            return f"Created file {filename}"
        except Exception as e:
            return f"touch: error creating file: {str(e)}"

    def rm(self, filename):
        try:
            file_path = os.path.join(self.current_path, filename).replace('\\', '/')
            if not self.vfs.file_exists(file_path):
                return f"rm: no such file: {filename}"
            self.vfs.delete_file(file_path)
            return f"Deleted file {filename}"
        except Exception as e:
            return f"rm: error deleting file: {str(e)}"


    def log_action(self, command, path, result):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        with open(self.config['log_file'], 'a', newline='') as log_file:
            writer = csv.writer(log_file)
            writer.writerow([timestamp, self.config['user'], command, path, result])