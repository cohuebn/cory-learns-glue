import sys
import re
from paintings import parse_episode
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.transforms import *
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.types import *
from pyspark.sql import Row
glueContext = GlueContext(SparkContext.getOrCreate())

# Static source records for testing
paintings_source = [
    ["S01E01","A WALK IN THE WOODS",0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0],
    ["S01E02","MT. MCKINLEY",0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,0]
]
paintings_schema = StructType([
  StructField("episode", StringType()),
  StructField("title", StringType()),
  StructField("apple_frame", LongType()),
  StructField("aurora_borealis", LongType()),
  StructField("barn", LongType()),
  StructField("beach", LongType()),
  StructField("boat", LongType()),
  StructField("bridge", LongType()),
  StructField("building", LongType()),
  StructField("bushes", LongType()),
  StructField("cabin", LongType()),
  StructField("cactus", LongType()),
  StructField("circle_frame", LongType()),
  StructField("cirrus", LongType()),
  StructField("cliff", LongType()),
  StructField("clouds", LongType()),
  StructField("conifer", LongType()),
  StructField("cumulus", LongType()),
  StructField("deciduous", LongType()),
  StructField("diane_andre", LongType()),
  StructField("dock", LongType()),
  StructField("double_oval_frame", LongType()),
  StructField("farm", LongType()),
  StructField("fence", LongType()),
  StructField("fire", LongType()),
  StructField("florida_frame", LongType()),
  StructField("flowers", LongType()),
  StructField("fog", LongType()),
  StructField("framed", LongType()),
  StructField("grass", LongType()),
  StructField("guest", LongType()),
  StructField("half_circle_frame", LongType()),
  StructField("half_oval_frame", LongType()),
  StructField("hills", LongType()),
  StructField("lake", LongType()),
  StructField("lakes", LongType()),
  StructField("lighthouse", LongType()),
  StructField("mill", LongType()),
  StructField("moon", LongType()),
  StructField("mountain", LongType()),
  StructField("mountains", LongType()),
  StructField("night", LongType()),
  StructField("ocean", LongType()),
  StructField("oval_frame", LongType()),
  StructField("palm_trees", LongType()),
  StructField("path", LongType()),
  StructField("person", LongType()),
  StructField("portrait", LongType()),
  StructField("rectangle_3d_frame", LongType()),
  StructField("rectangular_frame", LongType()),
  StructField("river", LongType()),
  StructField("rocks", LongType()),
  StructField("seashell_frame", LongType()),
  StructField("snow", LongType()),
  StructField("snowy_mountain", LongType()),
  StructField("split_frame", LongType()),
  StructField("steve_ross", LongType()),
  StructField("structure", LongType()),
  StructField("sun", LongType()),
  StructField("tomb_frame", LongType()),
  StructField("tree", LongType()),
  StructField("trees", LongType()),
  StructField("triple_frame", LongType()),
  StructField("waterfall", LongType()),
  StructField("waves", LongType()),
  StructField("windmill", LongType()),
  StructField("window_frame", LongType()),
  StructField("winter", LongType()),
  StructField("wood_framed", LongType())
])

paintings_data_frame = glueContext.createDataFrame(paintings_source, schema = paintings_schema)
paintings = DynamicFrame.fromDF(paintings_data_frame, glueContext, 'dyf')

# Cast all "bit" fields (LongTypes) into booleans
# It's easier to use a list of non-bit fields as the majority of fields imported are bit fields
non_bit_fields = ["episode", "title"]
bit_fields_specs = [
    (field.name, "cast:boolean")
    for field in paintings.schema()
    if field.name not in non_bit_fields and field.dataType.typeName() == 'long' # Type-check to provide accidentally casting a non-bit column if not in "non_bit_fields"
]
paintings_with_bool_fields = ResolveChoice.apply(paintings, specs = bit_fields_specs)

# Parse and clean up the season, episode, and episode text fields
# def normalize_episode_fields(record):
#     # Parse the season and episode numbers
#     season, episode = re.compile('S(\d+)E(\d+)').match(record['episode']).group(1, 2)
#     record['season_episode_text'] = record['episode']
#     record['season'] = int(season)
#     record['episode'] = int(episode)
#     record['title'] = record['title'].title()
#     return record
paintings_with_parsed_episodes = Map.apply(frame = paintings_with_bool_fields, f = parse_episode)

paintings_with_parsed_episodes.toDF().show()