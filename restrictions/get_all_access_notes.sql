SELECT DISTINCT resource.id
	, resource.ead_id
#    , note_persistent_id.persistent_id
    , rr.begin as Begin_Date
    , rr.end as End_Date
    , CAST(note.notes as CHAR (15000) CHARACTER SET UTF8) AS Text
    , CONCAT('/repositories/', resource.repo_id, '/resources/', resource.id) AS Resource_URL
FROM note
#LEFT JOIN note_persistent_id on note.id=note_persistent_id.note_id
LEFT JOIN resource on note.resource_id=resource.id
LEFT JOIN rights_restriction rr on rr.resource_id = resource.id
WHERE resource.repo_id = 12 #enter your repo_id here
AND note.notes LIKE '%accessrestrict%' 
OR note.notes LIKE '%userestrict%'
#OR (rr.restriction_note_type LIKE '%accessrestrict%' OR rr.restriction_note_type LIKE '%userestrict%');