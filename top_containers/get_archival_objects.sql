#added extra possibilities to account for various levels; MSSA has 9 levels at most...
SELECT resource.ead_id AS EAD_ID
	, resource.identifier AS Resource_ID
	, resource.title AS Collection_Title
    , aoj.display_string AS AO10
    , aoi.display_string AS AO09
    , aoh.display_string AS AO08
    , aog.display_string AS AO07
	, aof.display_string AS AO06
	, aoe.display_string AS AO05
	, aod.display_string AS AO04
	, aoc.display_string AS AO03
    , aob.display_string AS AO02
	, aoa.display_string AS AO01
	, ev.value AS AO_Level
	, CONCAT('/repositories/', resource.repo_id, '/resources/', resource.id) AS Resource_URL
	, CONCAT('/repositories/', resource.repo_id, '/archival_objects/', aoa.id) AS Archival_Object_URL
	from archival_object aoa
	left join archival_object aob on aob.id = aoa.parent_id
	left join archival_object aoc on aoc.id = aob.parent_id
	left join archival_object aod on aod.id = aoc.parent_id
	left join archival_object aoe on aoe.id = aod.parent_id
	left join archival_object aof on aof.id = aoe.parent_id
    left join archival_object aog on aog.id = aof.parent_id
    left join archival_object aoh on aoh.id = aog.parent_id
    left join archival_object aoi on aoi.id = aoh.parent_id
    left join archival_object aoj on aoj.id = aoi.parent_id
	left join resource on aoa.root_record_id = resource.id
	left join enumeration_value ev on ev.id= aoa.level_id
	WHERE resource.repo_id = 12 #enter your repo_id here
	AND resource.ead_id LIKE '%mssa.ms.0058%'
	Group by aoa.id