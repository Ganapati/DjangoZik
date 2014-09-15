rm ./db/db.sqlite3 ; touch ./db/db.sqlite3 && python ./manage.py syncdb && python ./manage.py cleansongs && python ./manage.py importmusic
