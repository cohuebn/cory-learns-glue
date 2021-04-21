from datetime import datetime

from awsglue import DynamicFrame
from awsglue.gluetypes import DynamicRecord


def with_current_timestamp(timestamp_column='current_timestamp'):
  """ Create a function capable of appending the current timestamp to all records in a DynamicFrame.
      This method returns a function so that it can be chained with other transformations
  :param timestamp_column: The name of the timestamp column in each record of a DynamicFrame
  :return: A function capable of adding the timestamp column to every record in a DynamicFrame
  """
  def current_timestamp_mapper(rec: DynamicRecord):
    rec[timestamp_column] = datetime.utcnow()
    return rec
  def operator(dynamic_frame: DynamicFrame) -> DynamicFrame:
    return dynamic_frame.map(f = current_timestamp_mapper)
  return operator
