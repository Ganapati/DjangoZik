rm ./db/db.sqlite3 ; touch ./db/db.sqlite3 && python ./manage.py syncdb && python ./manage.py importmusic && python ./manage.py importcovers && python ./manage.py importartists
