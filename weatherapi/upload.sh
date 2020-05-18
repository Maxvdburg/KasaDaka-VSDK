#!/bin/bash
expect -c "
spawn sftp group11@ict4d.saadittoh.com
expect \"password\"
send \"RYf6rLp243CgB7D6\r\"
expect \"sftp\"
send \"cd django\r\"
expect \"sftp\"
send \"put -r converted/\r\"
expect \"sftp\"
send \"exit\r\"
interact "
