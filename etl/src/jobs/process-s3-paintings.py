import sys
import re
from paintings import parse_episode
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.dynamicframe import DynamicFrame
from awsglue.utils import getResolvedOptions
from pyspark.sql.types import *
from pyspark.sql import Row
glueContext = GlueContext(SparkContext.getOrCreate())

args = getResolvedOptions(sys.argv, [ 'input_database', 'input_table', 'processed_bucket' ])

paintings = glueContext.create_dynamic_frame.from_catalog(
  database = args['input_database'],
  table_name = args['input_table']
)

# Cast all "bit" fields (LongTypes) into booleans
# It's easier to use a list of non-bit fields as the majority of fields imported are bit fields
non_bit_fields = ["episode", "title"]
bit_fields_specs = [
    (field.name, "cast:boolean")
    for field in paintings.schema()
    if field.name not in non_bit_fields and field.dataType.typeName() == 'long' # Type-check to provide accidentally casting a non-bit column if not in "non_bit_fields"
]
paintings_with_bool_fields = ResolveChoice.apply(paintings, specs = bit_fields_specs)
paintings_with_parsed_episodes = Map.apply(frame = paintings_with_bool_fields, f = parse_episode)

# Write the processed frame in Parquet format
glueContext.write_dynamic_frame.from_options(
  frame = paintings_with_parsed_episodes,
  connection_type = "s3",
  connection_options = {"path": f"s3://${args['processed_bucket']}/"},
  format = "parquet"
)