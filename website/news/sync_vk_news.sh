#!/bin/bash

cd /home/ivasio/profkom
source myvenv/bin/activate
cd website
python manage.py shell < news/sync_vk_news.py