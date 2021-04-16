from os.path import dirname, join

def get_test_file_path(filename):
  return join(dirname(__file__), filename)
