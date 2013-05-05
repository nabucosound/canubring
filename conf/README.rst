============
Installation
============

Check out the source::

    git clone git@github.com:nabucosound/canubring.git

Create virtual environment::

    mkvirtualenv canubring

Jump into project folder and install requirements::

    pip install -r requirements.txt

Copy the following files and follow their instructions inside to
edit them (the copied files, not the "_sample" ones!!!!)::

    cp conf/env_sample .env
    cp conf/localsettings_sample.py prj/localsettings.py
    vim .env
    vim prj/localsettings.py

Run the reset script corresponding to your db (sqlite or postgres)::

    ./scripts/reset_sqlite_db.sh

Start devel webserver and visit ``http://localhost:8000/``::

    python manage.py runserver

