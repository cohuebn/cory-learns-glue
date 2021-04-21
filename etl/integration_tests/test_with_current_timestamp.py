from datetime import datetime

from awsglue.context import GlueContext
from pyspark.context import SparkContext

from common.transforms.with_current_timestamp import with_current_timestamp
from .data import get_test_file_as_dynamic_frame

glueContext = GlueContext(SparkContext.getOrCreate())
logger = glueContext.get_logger()

def test_timestamp_addition_with_default_column():
  start_time = datetime.utcnow()
  dogs = get_test_file_as_dynamic_frame('dogs.csv', glueContext)
  dogs_with_timestamp = with_current_timestamp()(dogs)
  timestamp_values = [record['current_timestamp'] for record in dogs_with_timestamp.toDF().collect()]
  assert len(timestamp_values) == dogs.count()
  assertion_time = datetime.utcnow()
  assert all(start_time <= timestamp_value <= assertion_time for timestamp_value in timestamp_values)

def test_timestamp_addition_with_custom_column():
  start_time = datetime.utcnow()
  dogs = get_test_file_as_dynamic_frame('dogs.csv', glueContext)
  dogs_with_timestamp = with_current_timestamp('mowie_wowie')(dogs)
  timestamp_values = [record['mowie_wowie'] for record in dogs_with_timestamp.toDF().collect()]
  assert len(timestamp_values) == dogs.count()
  assertion_time = datetime.utcnow()
  assert all(start_time <= timestamp_value <= assertion_time for timestamp_value in timestamp_values)
