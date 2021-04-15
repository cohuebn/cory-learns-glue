import pytest
from paintings import parse_episode
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.types import *
from pyspark.sql import Row
glueContext = GlueContext(SparkContext.getOrCreate())

def test_bit_casting():
  # Static source records for testing
  paintings_source = [
    ["S01E01", "A WALK IN THE WOODS", 0, 0, 123],
    ["S01E02", "MT. MCKINLEY", 0, 0, 321]
  ]
  paintings_schema = StructType([
    StructField("episode", StringType()),
    StructField("title", StringType()),
    StructField("apple_frame", LongType()),
    StructField("aurora_borealis", LongType()),
    StructField("aurora_borealis", IntegerType())
  ])
  paintings_data_frame = glueContext.createDataFrame(paintings_source, schema=paintings_schema)
  paintings = DynamicFrame.fromDF(paintings_data_frame, glueContext, 'dyf')
  assert 1 == 83
