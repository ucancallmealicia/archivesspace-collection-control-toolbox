SELECT DISTINCT resource.ead_id AS EAD_ID
    , resource.identifier AS Identifier
    , resource.title AS Resource_Title
    , ev.value AS LEVEL
    , rr.restriction_note_type AS Restriction_Type
    , rr.begin AS BEGIN_DATE
    , rr.end AS END_DATE
    , CAST(note.notes as CHAR (10000) CHARACTER SET UTF8) AS restriction_text
    , CONCAT('/repositories/', resource.repo_id, '/resources/', resource.id) AS Resource_URL
FROM rights_restriction rr
LEFT JOIN resource on resource.id = rr.resource_id
LEFT JOIN enumeration_value ev on ev.id = resource.level_id
LEFT JOIN note on resource.id = note.resource_id
WHERE resource.repo_id = 12 #enter your repo_id here
AND rr.restriction_note_type LIKE '%accessrestrict%'
AND note.notes LIKE '%accessrestrict%'