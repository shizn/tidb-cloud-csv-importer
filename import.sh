#!/bin/bash
source ./.env
# Convert csv files into MariaDB using Python
pip install -r requirements.txt
python3 ./convert.py

# Dump a MySQL database to a file
printf "Dump to a local sql file\n"
mysqldump --column-statistics=0 -P 8083 --protocol=tcp -u root -p$DB_PASSWORD --databases $DB_NAME > $DB_NAME.sql

# Restore the database dump to another MySQL database
printf "Restore to TiDB Cloud, it might take several minutes due to your dataset size, please wait...\n"
mysql --connect-timeout 15 -u $TIDB_USERNAME -h $TIDB_HOST -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=$TIDB_SSL_CA -p$TIDB_PASSWORD < $DB_NAME.sql
printf "Done!\n"