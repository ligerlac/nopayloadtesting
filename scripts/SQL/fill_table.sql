TRUNCATE local_table;
INSERT INTO local_table(payload_list_id, major_iov, minor_iov, payload_url)
VALUES
 (0, 0, 0, 'pll0_0_0.dat'),
 (0, 1, 0, 'pll0_1_0.dat'),
 (0, 1, 1, 'pll0_1_1.dat'),
 (1, 1, 0, 'pll1_1_0.dat'),
 (1, 2, 3, 'pll1_2_3.dat'),
 (1, 0, 10, 'pll1_0_10.dat');
