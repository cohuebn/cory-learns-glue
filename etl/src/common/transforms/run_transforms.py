from functools import reduce

from awsglue import DynamicFrame


def run_transforms(dynamic_frame: DynamicFrame, *transforms) -> DynamicFrame:
  """ Run the provided transforms on the given dynamic frame.
      Each transform is expected to take in a DynamicFrame and output
      a DynamicFrame. This allows using the output of the previous transform
      as the input to the next transform in the series
  :param dynamic_frame: The DynamicFrame to transform
  :param transforms: The series of transforms to run on the given DynamicFrame
  :return: A DynamicFrame that is the result of running the series of transforms
    on the provided DynamicFrame
  """
  return reduce(lambda result, transform: transform(result), transforms, dynamic_frame)
