SELECT resource.ead_id AS EAD_ID
    , resource.identifier AS Resource_ID
    , resource.title AS Collection_Title
    , ao.display_string AS Archival_Object_Title
    , ev2.value AS AO_Level
    , CONCAT('/repositories/', resource.repo_id, '/resources/', resource.id) AS Resource_URL
    , CONCAT('/repositories/', resource.repo_id, '/archival_objects/', ao.id) AS Archival_Object_URL
    , tc.barcode AS Barcode
    , cp.name AS Container_Type
    , tc.indicator AS Container_Number
    , ev3.value AS Sub_Container_Type
    , sc.indicator_2 AS Sub_Container_Indicator
from sub_container sc
left join enumeration_value on enumeration_value.id = sc.type_2_id
left join top_container_link_rlshp tclr on tclr.sub_container_id = sc.id
left join top_container tc on tclr.top_container_id = tc.id
left join top_container_profile_rlshp tcpr on tcpr.top_container_id = tc.id
left join container_profile cp on cp.id = tcpr.container_profile_id
left join location on location.barcode = tc.barcode
left join instance on sc.instance_id = instance.id
left join archival_object ao on instance.archival_object_id = ao.id
left join resource on ao.root_record_id = resource.id
left join repository on repository.id = resource.repo_id
left join enumeration_value ev2 on ev2.id = ao.level_id
left join enumeration_value ev3 on ev3.id = sc.type_2_id
WHERE resource.repo_id = 12 #your repo_id goes here
AND resource.ead_id LIKE '%mssa.ms.0598%' #your ead_id goes here
ORDER BY Archival_Object_URL