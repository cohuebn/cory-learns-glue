-- Get the most recent version of all paintings containing either mountains, waterfalls, or the sun.
-- Order results with the ones containing the most of these characteristics at the top
with resolved_paintings_processed as (
  SELECT *,
         row_number() over (partition by season, episode order by ingestion_timestamp desc) as row_num
  FROM "glue-learning-paintings"."glue_learning_paintings_processed"
),
matches_criteria as (
  select title, season, episode, waterfall, mountain, clouds,
   cast(waterfall as tinyint) + cast(mountain as tinyint) + cast(clouds as tinyint) match_count
  from resolved_paintings_processed
  where row_num = 1
  and (waterfall = true or mountain = true or clouds = true)
)
select title, season, episode, waterfall, mountain, clouds
from matches_criteria
order by match_count desc, mountain desc, waterfall desc
