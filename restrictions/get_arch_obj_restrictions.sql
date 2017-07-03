SELECT resource.ead_id AS EAD_ID
    , resource.identifier AS Identifier
    , resource.title AS Resource_Title
    , ev.value AS LEVEL
    , ao.display_string AS Object_Title
    , rr.restriction_note_type AS Restriction_Type
	, rr.begin AS BEGIN_DATE
    , rr.end AS END_DATE
    , CAST(note.notes as CHAR (10000) CHARACTER SET UTF8) AS restriction_text
    , CONCAT('/repositories/', resource.repo_id, '/resources/', resource.id) AS Resource_URL
    , CONCAT('/repositories/', resource.repo_id, 'archival_objects/', ao.id) AS Archival_Object_URL
FROM rights_restriction rr
LEFT JOIN archival_object ao on ao.id = rr.archival_object_id
LEFT JOIN resource on ao.root_record_id = resource.id
LEFT JOIN enumeration_value ev on ev.id = ao.level_id
LEFT JOIN note on ao.id = note.archival_object_id
WHERE resource.repo_id = 12 #enter your repo ID here
AND rr.restriction_note_type LIKE '%accessrestrict%'