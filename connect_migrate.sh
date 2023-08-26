#!/bin/bash

set -e

### information to populate
###
WYZE_EMAIL=youremail
WYZE_PASSWORD=yourpassword
WYZE_KEY_ID=your_ID
WYZE_API_KEY=your_key
Garmin_username=youremail
Garmin_password=yourpassword
export PATH="$HOME/.local/bin:$PATH"
export WYZE_EMAIL
export WYZE_PASSWORD
export WYZE_KEY_ID
export WYZE_API_KEY
cd ~/path_to_your_script/
###
### end of information to populate

mkdir migrate_data

python3 ./scale_migrate.py

for fname in migrate_data/*.fit ; do
  echo "uploading $fname ..."

  if gupload -u $Garmin_username -p $Garmin_password  -v 1 "$fname"; then
    echo "uploaded $fname"
  else
    echo "failed uploading $fname"
    exit 1
  fi
  
done

