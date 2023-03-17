SELECT m.payload_list_id, m.payload_url, m.major_iov, t.majx, m.minor_iov
FROM (
  SELECT payload_list_id, MAX(major_iov) AS majx
  FROM "PayloadIOV"
  GROUP BY payload_list_id
) t JOIN "PayloadIOV" m ON m.payload_list_id = t.payload_list_id AND t.majx = m.major_iov
;
