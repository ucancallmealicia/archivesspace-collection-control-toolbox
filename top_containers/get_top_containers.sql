SELECT tc.barcode as barcode
    , cp.name as container_profile_name
    , tc.indicator as indicator
    , location.title as location_name
    , CONCAT('/locations/', location.id) as location_uri
    , CONCAT('/container_profiles/', tcpr.container_profile_id) as container_profile_uri
    , CONCAT('/repositories/', tc.repo_id, '/top_containers/', tc.id) as top_container_uri
FROM top_container tc
LEFT JOIN top_container_housed_at_rlshp tchr on tchr.top_container_id = tc.id
LEFT JOIN location on tchr.location_id = location.id
LEFT JOIN top_container_profile_rlshp tcpr on tcpr.top_container_id = tc.id
LEFT JOIN container_profile cp on cp.id = tcpr.container_profile_id
WHERE tc.repo_id = 12 #your repo_id goes here
ORDER BY top_container_uri