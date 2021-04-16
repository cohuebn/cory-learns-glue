from paintings import process_paintings
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.types import *
glueContext = GlueContext(SparkContext.getOrCreate())

# Static source records for testing
paintings_schema = StructType([
  StructField("episode", StringType()),
  StructField("title", StringType()),
  StructField("apple_frame", LongType()),
  StructField("aurora_borealis", LongType()),
  StructField("an_unmapped_field", IntegerType())
])
paintings_source = [
  ["S01E01", "A WALK IN THE WOODS", 1, 0, 123],
  ["S03E13", "PEACEFUL WATERS", 0, 1, 321]
]

def _find_row(paintings: DynamicFrame, episode_text: str):
  """ Assert a given row exists in the dynamic frame and that it contains the expected values """
  matches = paintings.filter(lambda x: x['season_episode_text'] == episode_text).toDF().collect()
  assert len(matches) == 1
  return matches[0]

def test_episode_parsing():
  paintings_data_frame = glueContext.createDataFrame(paintings_source, schema=paintings_schema)
  paintings = DynamicFrame.fromDF(paintings_data_frame, glueContext, 'paintings')
  transformed_paintings = process_paintings(paintings)
  assert transformed_paintings.count() == 2
  first_episode = _find_row(transformed_paintings, 'S01E01')
  assert first_episode['season'] == 1
  assert first_episode['episode'] == 1
  assert first_episode['title'] == 'A Walk In The Woods'
  second_episode = _find_row(transformed_paintings, 'S03E13')
  assert second_episode['season'] == 3
  assert second_episode['episode'] == 13
  assert second_episode['title'] == 'Peaceful Waters'

def test_boolean_casting():
  paintings_data_frame = glueContext.createDataFrame(paintings_source, schema=paintings_schema)
  paintings = DynamicFrame.fromDF(paintings_data_frame, glueContext, 'paintings')
  transformed_paintings = process_paintings(paintings)
  assert transformed_paintings.count() == 2
  first_episode = _find_row(transformed_paintings, 'S01E01')
  assert first_episode['apple_frame'] == True
  assert first_episode['aurora_borealis'] == False
  assert first_episode['an_unmapped_field'] == 123
  second_episode = _find_row(transformed_paintings, 'S03E13')
  assert second_episode['apple_frame'] == False
  assert second_episode['aurora_borealis'] == True
  assert second_episode['an_unmapped_field'] == 321
