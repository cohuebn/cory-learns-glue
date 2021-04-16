import pytest
from paintings.parse_episode import parse_episode

def test_extracting_season_and_episode_number():
  record = { 'episode': 'S02E13', 'title': 'MT. MCKINLEY' }
  updated_record = parse_episode(record)
  assert updated_record['season_episode_text'] == 'S02E13'
  assert updated_record['season'] == 2
  assert updated_record['episode'] == 13

episode_name_test_cases = [
  # TODO - evaluate if the titlecase pip module could be used and work better here
  ('A WALK IN THE WOODS', 'A Walk In The Woods'),
  ('MT. MCKINLEY', 'Mt. Mckinley'),
  ('MOUNTAIN BLOSSOMS', 'Mountain Blossoms')
]
@pytest.mark.parametrize('original_title,output_title', episode_name_test_cases)
def test_cleaning_up_episode_name(original_title, output_title):
  record = { 'episode': 'S02E13', 'title': original_title }
  updated_record = parse_episode(record)

  assert updated_record['title'] == output_title
