curl http://localhost:8000/api/cdb_rest/globalTags | json_pp
curl -X DELETE "http://localhost:8000/api/cdb_rest/deleteGlobalTag/global_tag_9858"
curl -X POST "http://localhost:8000/api/cdb_rest/cloneGlobalTag/my_gt/clone_1"