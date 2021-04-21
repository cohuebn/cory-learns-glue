from awsglue.context import GlueContext
from pyspark.context import SparkContext

from common.transforms.with_filename import with_filename
from .data import get_test_file_path, get_test_file_as_dynamic_frame


glueContext = GlueContext(SparkContext.getOrCreate())
logger = glueContext.get_logger()

def test_filename_addition_with_default_column():
  dogs = get_test_file_as_dynamic_frame('dogs.csv', glueContext)
  dogs_with_filename = with_filename(glueContext)(dogs)
  input_file_names = [record['source_file_name'] for record in dogs_with_filename.toDF().collect()]
  assert len(input_file_names) == dogs.count()
  expected_file_path = f'file://{get_test_file_path("dogs.csv")}'
  assert all(input_file_name == expected_file_path for input_file_name in input_file_names)

def test_filename_addition_with_custom_column():
  dogs = get_test_file_as_dynamic_frame('dogs.csv', glueContext)
  dogs_with_filename = with_filename(glueContext, 'snippy-snaps')(dogs)
  input_file_names = [record['snippy-snaps'] for record in dogs_with_filename.toDF().collect()]
  assert len(input_file_names) == dogs.count()
  expected_file_path = f'file://{get_test_file_path("dogs.csv")}'
  assert all(input_file_name == expected_file_path for input_file_name in input_file_names)
