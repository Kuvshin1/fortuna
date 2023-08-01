import os


def from_module_path_to(relative_path):
  absolute_path = os.path.dirname(__file__)
  return os.path.join(absolute_path, f"../{relative_path}")
