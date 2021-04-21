from awsglue import DynamicFrame
from awsglue.transforms import ResolveChoice, Map

from .parse_episode import parse_episode

def process_paintings(paintings: DynamicFrame) -> DynamicFrame:
  # Cast all "bit" fields (LongTypes) into booleans
  # It's easier to use a list of non-bit fields as the majority of fields imported are bit fields
  non_bit_fields = ["episode", "title"]
  bit_fields_specs = [
      (field.name, "cast:boolean")
      for field in paintings.schema()
      if field.name not in non_bit_fields and field.dataType.typeName() == 'long'
  ]
  paintings_with_bool_fields = ResolveChoice.apply(paintings,
                                                   specs = bit_fields_specs,
                                                   transformation_ctx = "paintings_with_bool_cast")
  paintings_with_parsed_episodes = Map.apply(frame = paintings_with_bool_fields,
                                             f = parse_episode,
                                             transformation_ctx = "paintings_with_parsed_episodes")
  return paintings_with_parsed_episodes
