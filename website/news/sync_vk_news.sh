#!/bin/bash

cd ~/profkom
source myvenv/bin/activate
cd website

if test "$1" = "reload"
then
    python manage.py shell < news/reload_vk_news.py
else
	python manage.py shell < news/sync_vk_news.py
fi
