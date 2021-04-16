import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

from paintings.process_paintings import process_paintings

args = getResolvedOptions(sys.argv, [ 'JOB_NAME', 'input_database', 'input_table', 'processed_bucket' ])
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

paintings = glueContext.create_dynamic_frame.from_catalog(
  database = args['input_database'],
  table_name = args['input_table'],
  transformation_ctx = "paintings-source"
)

transformed_paintings = process_paintings(paintings)

# Write the processed frame in Parquet format
glueContext.write_dynamic_frame.from_options(
  frame = transformed_paintings,
  connection_type = 's3',
  connection_options = { 'path': 's3://' + args["processed_bucket"] + '/', 'partitionKeys': ['season'] },
  format = "glueparquet",
  transformation_ctx = "paintings-sink"
)
job.commit()
