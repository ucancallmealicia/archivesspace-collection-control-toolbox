#This SQL script retrieves a list of container profiles from the ArchivesSpace database
#The container profile URIs from this list can be used to add container profiles to your 
#top containers in the create_top_container.py script included this toolbox

SELECT cp.name
    , cp.extent_dimension
    , cp.height
    , cp.width
    , cp.depth
    , ev.value as dimension_units
    , CONCAT('/container_profiles/', cp.id) as container_profile_URI
FROM container_profile cp
LEFT JOIN enumeration_value ev on ev.id = cp.dimension_units_id
