from common.add_filename import add_filename
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame

from .data import get_test_file_path

glueContext = GlueContext(SparkContext.getOrCreate())
logger = glueContext.get_logger()

def _find_row(dogs: DynamicFrame, breed: str):
  """ Assert a given row exists in the dynamic frame and that it contains the expected values """
  matches = dogs.filter(lambda x: x['breed'] == breed).toDF().collect()
  assert len(matches) == 1
  return matches[0]

def test_filename_addition_with_default_column():
  dogs_file_path = get_test_file_path('dogs.csv')
  dogs_data_frame = glueContext.spark_session.read.csv(dogs_file_path, header=True)
  dogs = DynamicFrame.fromDF(dogs_data_frame, glueContext, 'incoming-dogs')
  dogs_with_filename = add_filename(dogs, glueContext)
  input_file_names = [record['source_file_name'] for record in dogs_with_filename.toDF().collect()]
  assert len(input_file_names) == dogs_data_frame.count()
  expected_file_path = f'file://{dogs_file_path}'
  assert all(input_file_name == expected_file_path for input_file_name in input_file_names)

def test_filename_addition_with_custom_column():
  dogs_file_path = get_test_file_path('dogs.csv')
  dogs_data_frame = glueContext.spark_session.read.csv(dogs_file_path, header=True)
  dogs = DynamicFrame.fromDF(dogs_data_frame, glueContext, 'incoming-dogs')
  dogs_with_filename = add_filename(dogs, glueContext, 'snippy-snaps')
  input_file_names = [record['snippy-snaps'] for record in dogs_with_filename.toDF().collect()]
  assert len(input_file_names) == dogs_data_frame.count()
  expected_file_path = f'file://{dogs_file_path}'
  assert all(input_file_name == expected_file_path for input_file_name in input_file_names)
