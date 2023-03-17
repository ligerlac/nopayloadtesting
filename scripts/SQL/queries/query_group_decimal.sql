\set my_gt 'my_gt'
\set my_major_iov 10000000000
\set my_minorr_iov 10000000000

CREATE FUNCTION myfunc(a bigint, b bigint) RETURNS float
  RETURN a + CAST(b AS float) / 10000000000;

SELECT m.payload_list_id, m.payload_url, m.major_iov, m.minor_iov--, t.f_max
FROM (
    SELECT payload_list_id, MAX(myfunc(major_iov, minor_iov)) AS f_max
    FROM "PayloadIOV"
    WHERE myfunc(major_iov, minor_iov) <= myfunc(:my_major_iov, :my_minor_iov)
    AND payload_list_id IN (
        SELECT id FROM "PayloadList"
        WHERE global_tag_id = (
            SELECT id FROM "GlobalTag"
            WHERE name=:'my_gt'
        )
    )
GROUP BY payload_list_id
) t JOIN "PayloadIOV" m ON m.payload_list_id = t.payload_list_id AND t.f_max = myfunc(m.major_iov, m.minor_iov)
