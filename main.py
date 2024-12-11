import csv
from shell import Shell
from shell_gui import ShellGUI
import tkinter as tk
import argparse

def load_config_from_csv(user, vfs_path, log_file):
    config = {
        'user': user,
        'vfs_path': vfs_path,
        'log_file': log_file
    }
    return config

def main():
    parser = argparse.ArgumentParser(description='Emulator for shell commands.')
    parser.add_argument('--user', '-u', required=True, help='User name for the shell prompt.')
    parser.add_argument('--vfs', '-v', required=True, help='Path to the zip archive for VFS.')
    parser.add_argument('--log', '-l', required=True, help='Path to the log file (CSV format).')

    args = parser.parse_args()

    # Загружаем конфигурацию из командной строки
    config = load_config_from_csv(args.user, args.vfs, args.log)

    shell = Shell(config)

    root = tk.Tk()
    gui = ShellGUI(root, shell)
    gui.run()


if __name__ == "__main__":
    main()