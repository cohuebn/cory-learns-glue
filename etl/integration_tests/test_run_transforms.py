from datetime import datetime

from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext

from common.transforms.run_transforms import run_transforms
from .data import get_test_file_as_dynamic_frame

glueContext = GlueContext(SparkContext.getOrCreate())
logger = glueContext.get_logger()

def _find_row(dogs: DynamicFrame, breed: str):
  """ Find the only row matching the given breed in the Dynamic Frame of dog records
      If no rows exist or more than one row exists with the given breed, fail the test
  """
  matches = dogs.filter(lambda x: x['breed'] == breed).toDF().collect()
  assert len(matches) == 1
  return matches[0]

# Fake transform for testing
def _enhance_bark_strength(dynamic_frame: DynamicFrame) -> DynamicFrame:
  def bark_strength_record_enhancer(record):
    record['bark_strength'] = int(record['bark_strength']) + 2
    return record
  return dynamic_frame.map(f = bark_strength_record_enhancer)

# Fake transform for testing
def _add_sophisticated_name(dynamic_frame: DynamicFrame) -> DynamicFrame:
  def sophisticated_name_record_adder(record):
    record['sophisticated_name'] = f'Sir {record["best_name"].title()} III'
    return record
  return dynamic_frame.map(f = sophisticated_name_record_adder)

def test_chained_transforms():
  dogs = get_test_file_as_dynamic_frame('dogs.csv', glueContext)
  transformed_dogs = run_transforms(dogs, _enhance_bark_strength, _add_sophisticated_name)
  assert transformed_dogs.count() == dogs.count()
  great_dane = _find_row(transformed_dogs, 'great dane')
  assert great_dane['bark_strength'] == 11
  assert great_dane['sophisticated_name'] == 'Sir Marmaduke III'
