#!/usr/bin/bash
bu_date=$(date +%Y-%m-%d_%H%M%S)
backup_dir="${BACKUP_DIR:=backups}"
mkdir -p $backup_dir

container="${DB_CONTAINER:=db}"
db_user="${DB_USER:=postgres}"
db_name="${DB_NAME:=postgres}"
file_name="backup_${bu_date}.sql"
docker exec -t $container pg_dump -U $db_user $db_name > $backup_dir/$file_name