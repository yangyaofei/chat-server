import os


def get_project_path():
    """
    :return: 工程所在目录
    """
    return os.path.abspath(os.path.dirname(__file__))

