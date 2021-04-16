from awsglue.context import GlueContext
from pyspark.sql.functions import input_file_name
from awsglue.dynamicframe import DynamicFrame

def add_filename(dynamic_frame: DynamicFrame, glue_ctx: GlueContext, input_file_name_column='source_file_name'):
  """ Add the input filename to the given dynamic frame
  :param dynamic_frame: The incoming dynamic frame
  :param glue_ctx: The Glue context
  :param input_file_name_column: The name of the column to add that contains the input filename
  :return: A new dynamic frame containing the original data with an additional column
    containing the input filename
  """
  with_input_filename = dynamic_frame.toDF().withColumn(input_file_name_column, input_file_name())
  return DynamicFrame.fromDF(with_input_filename, glue_ctx, f'{dynamic_frame.name}-with-source-filename')
