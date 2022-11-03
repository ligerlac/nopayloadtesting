# in one shell
ssh -L 2222:spool0001.sdcc.bnl.gov:22 lgerlach1@ssh.sdcc.bnl.gov -i ~/.ssh/id_rsa_sdcc

# in another shell
ssh -p 2222 lgerlach1@localhost

# copy file via safe file transfer
sftp -r -i ~/.ssh/id_rsa_sdcc lgerlach1@sftp.sdcc.bnl.gov:/lbne/u/lgerlach1/Projects/nopayloadtesting/output/* output/

