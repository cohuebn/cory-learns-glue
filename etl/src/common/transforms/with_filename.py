from awsglue import DynamicFrame
from awsglue.context import GlueContext
from pyspark.sql.functions import input_file_name


def with_filename(glue_ctx: GlueContext,
                  input_file_name_column='source_file_name',
                  output_dynamic_frame_name=None):
  """ Create a function capable of appending the input filename to all records in a DynamicFrame.
      This method returns a function so that it can be chained it with other transformations
  :param glue_ctx: The Glue context
  :param input_file_name_column: The name of the column to add that contains the input filename
  :param output_dynamic_frame_name: The name of the dynamic frame output from this transformation.
    If not specified, "-with-{input_file_name_column}" will be appended to the end of the
    input Dynamic Frame's name
  :return: A function capable of adding the input filename column to every record in a DynamicFrame
  """
  def operator(dynamic_frame: DynamicFrame) -> DynamicFrame:
    including_input_filename = dynamic_frame.toDF().withColumn(input_file_name_column, input_file_name())
    return DynamicFrame.fromDF(including_input_filename, glue_ctx,
                               output_dynamic_frame_name or f'{dynamic_frame.name}-with-{input_file_name_column}')
  return operator
