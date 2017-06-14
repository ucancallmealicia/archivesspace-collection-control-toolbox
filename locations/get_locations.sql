SELECT title
	, building
    , floor
    , room
    , area
	, coordinate_1_label
    , coordinate_1_indicator
	, coordinate_2_label
    , coordinate_2_indicator
    , coordinate_3_label
    , coordinate_3_indicator
    , CONCAT('/locations/', id) as location_URI
FROM location