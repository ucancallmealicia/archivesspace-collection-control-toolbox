SELECT l.title
	, l.building
    , l.floor
    , l.room
    , l.area
	, l.coordinate_1_label
    , l.coordinate_1_indicator
	, l.coordinate_2_label
    , l.coordinate_2_indicator
    , l.coordinate_3_label
    , l.coordinate_3_indicator
    , CONCAT('/locations/', l.id) as location_URI
    , CONCAT('/location_profiles', lp.id) as location_profile_URI
FROM location l
LEFT JOIN location_profile_rlshp lpr on lpr.location_id = l.id
LEFT JOIN location_profile lp on lp.id = lpr.location_profile_id