import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

from common.transforms.run_transforms import run_transforms
from common.transforms.with_filename import with_filename
from common.transforms.with_current_timestamp import with_current_timestamp
from paintings.process_paintings import process_paintings

args = getResolvedOptions(sys.argv, [ 'JOB_NAME', 'input_database', 'input_table', 'processed_bucket' ])
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# optimal_parquet_size_in_bytes = 1048576 * 512
paintings = glueContext.create_dynamic_frame.from_catalog(
  database = args['input_database'],
  table_name = args['input_table'],
  transformation_ctx = "paintings-source"
)

transformed_paintings = run_transforms(paintings,
                                       with_current_timestamp('ingestion_timestamp'),
                                       with_filename(glueContext),
                                       process_paintings)

# Write the processed frame in Parquet format
glueContext.write_dynamic_frame.from_options(
  frame = transformed_paintings,
  connection_type = 's3',
  connection_options = {'path': f's3://{args["processed_bucket"]}/'},
  format = "glueparquet",
  transformation_ctx = "paintings-sink"
)
job.commit()
