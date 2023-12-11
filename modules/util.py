import subprocess
import platform

def open_file(file_path):
    if platform.system() == 'Darwin':  # macOS
        subprocess.run(['open', file_path])
    elif platform.system() == 'Windows':
        subprocess.run(['start', '', file_path], shell=True)
    elif platform.system() == 'Linux':
        subprocess.run(['xdg-open', file_path])