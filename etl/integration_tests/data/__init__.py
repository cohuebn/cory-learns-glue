from os.path import dirname, join

from awsglue import DynamicFrame


def get_test_file_path(filename):
  return join(dirname(__file__), filename)

def get_test_file_as_dynamic_frame(filename, glue_context):
  test_filepath = get_test_file_path(filename)
  data_frame = glue_context.spark_session.read.csv(test_filepath, header=True)
  return DynamicFrame.fromDF(data_frame, glue_context, 'df')
