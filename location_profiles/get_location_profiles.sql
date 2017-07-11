SELECT lp.name
	, lp.depth
    , lp.width
    , lp.height
	, ev.value AS dimension_units
    , CONCAT('/location_profiles/', lp.id) AS location_profile_URI
FROM location_profile lp
LEFT JOIN enumeration_value ev on ev.id = lp.dimension_units_id