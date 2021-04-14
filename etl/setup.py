from setuptools import setup, find_packages

setup(
  name="cory.etl",
  author="Cory Huebner",
  description="A pretend ETl that I made up so I could learn how to use Glue",
  url="https://github.com/cohuebn/cory-learns-glue",
  version='0.0.1',
  packages = find_packages(
    where = 'src'
  ),
  package_dir = {"":"src"}
)
