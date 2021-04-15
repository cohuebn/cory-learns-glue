#!/usr/bin/env python
# There isn't currently a pip-compatible glue package. This script just downloads the package and add it to the
# requested output directory

import argparse
import os
import re
import tarfile
import tempfile
import urllib.request

current_dir = os.path.dirname(__file__)
default_output_dir = os.path.join(current_dir, 'venv/lib/python3.7/site-packages')

parser = argparse.ArgumentParser(description='Install the Glue Python modules (currently no pip-compatible package exists.')
parser.add_argument('--source_url', type=str,
                    default='https://github.com/awslabs/aws-glue-libs/archive/refs/heads/glue-1.0.tar.gz',
                    help='The source url (expecting a tar gz file) that contains the glue source')
parser.add_argument('--output_dir', type=str,
                    default=default_output_dir,
                    help='Where should the output Glue modules be copied?')

args = parser.parse_args()
source_url, output_dir = args.source_url, args.output_dir

with urllib.request.urlopen(source_url) as source_response, \
     tempfile.NamedTemporaryFile() as source_file:
  source_file.write(source_response.read())
  with tarfile.open(name=source_file.name, mode="r:gz") as source_targz:
    for tarinfo in source_targz.getmembers():
      if re.search(r"/awsglue/.*\.py", tarinfo.name):
        source_targz.extract(member=tarinfo.name, path=output_dir)
  os.rename(os.path.join(output_dir, "aws-glue-libs-glue-1.0/awsglue"), os.path.join(output_dir, "awsglue"))
  os.rmdir(os.path.join(output_dir, 'aws-glue-libs-glue-1.0'))
