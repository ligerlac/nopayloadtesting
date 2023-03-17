\set my_gt 'my_gt'
\set my_major_iov 10000000000
\set my_minor_iov 10000000000

WITH major_max_table AS(
    SELECT m.payload_list_id, m.payload_url, m.major_iov, m.minor_iov, t.major_max--, l.name
    FROM (
        SELECT payload_list_id, MAX(major_iov) AS major_max
        FROM "PayloadIOV"
        WHERE ((major_iov < :my_major_iov) OR (major_iov = :my_major_iov AND minor_iov <= :my_minor_iov))
        AND payload_list_id IN (
            SELECT id FROM "PayloadList"
            WHERE global_tag_id = (
                SELECT id FROM "GlobalTag"
                WHERE name=:'my_gt'
            )
        )
    GROUP BY payload_list_id
    ) t JOIN "PayloadIOV" m ON m.payload_list_id = t.payload_list_id AND t.major_max = m.major_iov
),

major_minor_max_table AS(
    SELECT n.payload_list_id, n.payload_url, n.major_iov, n.minor_iov
    FROM (
        SELECT payload_list_id, MAX(minor_iov) AS minor_max
        FROM major_max_table
        GROUP BY payload_list_id
    ) u JOIN major_max_table n ON n.payload_list_id = u.payload_list_id AND u.minor_max = n.minor_iov
)

SELECT y.name AS payload_type_name, x.payload_url, x.major_iov, x.minor_iov
FROM 
  major_minor_max_table x 
  JOIN "PayloadList" z ON x.payload_list_id = z.id
  JOIN "PayloadType" y ON z.payload_type_id = y.id
;

