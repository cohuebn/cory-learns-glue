import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

from paintings.process_paintings import process_paintings
from common.add_filename import add_filename

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

transformed_paintings = process_paintings(
  add_filename(paintings, glueContext)
)

# Write the processed frame in Parquet format
optimal_parquet_size_in_bytes = 1048576 * 512
glueContext.write_dynamic_frame.from_options(
  frame = transformed_paintings,
  connection_type = 's3',
  connection_options = {'path': f's3://{args["processed_bucket"]}/'},
  format = "glueparquet",
  transformation_ctx = "paintings-sink"
)
job.commit()
