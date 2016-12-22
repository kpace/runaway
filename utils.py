import os, config


def get_style():
    with open(os.path.join(config.PROJECT_ROOT, 'gui/resources/style.qss'), 'r') as file:
        return file.read()
