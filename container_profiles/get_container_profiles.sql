SELECT cp.name
    , cp.extent_dimension
    , cp.height
    , cp.width
    , cp.depth
    , ev.value as dimension_units
    , CONCAT('/container_profiles/', cp.id) as container_profile_URI
FROM container_profile cp
LEFT JOIN enumeration_value ev on ev.id = cp.dimension_units_id