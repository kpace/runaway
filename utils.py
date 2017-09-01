import config
import os


def get_style():
    with open(
            os.path.join(config.PROJECT_ROOT, 'gui/resources/style.qss'),
            'r') as file:
        return file.read()


def get_record():
    with open(os.path.join(config.PROJECT_ROOT, 'game_data.dat'), 'r') as f:
        return int(f.readline())


def save_record(points):
    with open(os.path.join(config.PROJECT_ROOT, 'game_data.dat'), 'w') as f:
        f.write(str(points))
