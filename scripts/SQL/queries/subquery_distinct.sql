SELECT DISTINCT ON (payload_list_id)
  payload_list_id, payload_url, major_iov
FROM
  "PayloadIOV"
ORDER BY
  payload_list_id, major_iov DESC;
