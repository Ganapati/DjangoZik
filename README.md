DjangoZik
=========

web music player (mp3, ogg)

How to start :
--------------
1. Change MUSIC_PATH in djangozik/settings.py to match your music folder
2. Change SECRET_KEY (ofc)
3. pip install -r requirements.txt
4. Run reset.sh (keep cool, it can be very long (parsing existing mp3))
5. Profit !

Why not a cloud-bigdata-(insert buzzword here) connected application ?
----------------------------------------------------------------------
I believe in self-hosted solutions.
I don't like dropbox, google drive, skydrive and all that shit.

Do you really want to host your music on random server without any control (except from big company with fuzzy terms of use) ?
I like to own and share my data, without any arbitrary restrictions.

DjangoZik will never have connectors to theses services on my branch.
But if you really want to have theses features, write it yourself and share it !

(Same thing with youtube, soundcloud and co.)

TODO :
------

1. Change UI
2. Share music between remote instances (add REST API, connectors and stuff)
