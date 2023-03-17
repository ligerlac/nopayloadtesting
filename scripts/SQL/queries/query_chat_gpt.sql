\set my_gt 'my_small_gt'
\set my_major_iov 10000000000
\set my_minor_iov 10000000000

SELECT
    p.payload_url,
    t.name
FROM
    (
        SELECT
            MAX(pio.minor_iov) AS minor_max,
            pio.payload_list_id
        FROM
            "PayloadIOV" AS pio
            JOIN "PayloadList" AS pl ON pio.payload_list_id = pl.id
            JOIN "GlobalTag" AS gt ON pl.global_tag_id = gt.id
        WHERE
            gt.name = :'my_gt'
            AND (
                pio.major_iov < :my_major_iov
                OR (pio.major_iov = :my_major_iov AND pio.minor_iov <= :my_minor_iov)
            )
        GROUP BY
            pio.payload_list_id
    ) AS max_minor_iov
    JOIN "PayloadIOV" AS p ON (
        p.payload_list_id = max_minor_iov.payload_list_id
        AND p.minor_iov = max_minor_iov.minor_max
    )
    JOIN "PayloadList" AS pl ON p.payload_list_id = pl.id
    JOIN "PayloadType" AS t ON pl.payload_type_id = t.id
;
