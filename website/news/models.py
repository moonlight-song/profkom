'''
from django.db import models
import requests
from django.contrib.auth.models import User
from aldryn_people.models import Person
from django.utils.safestring import SafeText
from aldryn_newsblog.models import Article
from os.path import join as path_join
from filer.management.commands.import_files import FileImporter


VK_URL_TEMPLATE = "https://api.vk.com/method/{method_name}?{parameters}&access_token={access_token}&v={api_version}"


def retrieveAcessToken():
	return "6160b92c6160b92c6160b92c9261053238661606160b92c3a0916672b1e9ddd8d1fc1ed"


def checkVkPosts(request):
	
	url = VK_URL_TEMPLATE.format (method_name = "wall.get", api_version = "5.60", parameters = "domain=profkom_phystech",
		access_token = retrieveAcessToken())
	response = requests.get(url)
	#r.status_code
	response_data = response.json()
	posts = response_data['response']['items']
	posts_to_load = []

	for post in posts :
		if len(post.copy_history) != 0 : continue
		if postAlreadyLoaded(post.post_id) : continue
		posts_to_load.append(post)

	return importVkPost (posts_to_load[0])


def importVkPost(post):

	title = post['text'][0:100]
	title = title[0:title.rfind (' ')]

	try :
		attachment = post['attachments'][0]
		photo_key = ""
		for key in attachment['photo'] : 
			if 'photo_' in key : photo_key = key
		pic_url = attachment['photo'][key]

		# Check whether it is a picture
		header = requests.head(pic_url, allow_redirects=True)
		if 'image' not in header.headers.get('content-type').lower() :
			raise Exception()

		pic_response = requests.get(pic_url, allow_redirects=True)
		url_end_index = pic_url.find('.com')
		path_to_save = pic_url[url_end_index + 5 : -1].replace('/', '_')
		
		pic_file = open(path_join(MEDIA_URL, 'vk_pictures', path_to_save), 'rwb')
		pic_file.write(pic_response.content)

		importer = FileImporter()
		folder = FileImporter.get_or_create_folder(importer, ['base', 'subfolder'])
		file_obj = DjangoFile(pic_file, name = title +'.jpg')
		pic = importer.import_file(file_obj, folder)
		pic.save()
		pic_file.close()

	except :
		pic = None

	safetext = SafeText(post['text'])
	author = Person.objects.language('ru-ru').all()[0]
	config = NewsBlogConfig.objects.language('ru-ru').all()[0]

	article = Article(author = author, app_config = config, owner = author.user, 
		title = title, featured_image = pic, lead_in = safetext)
	article.set_current_language('ru-ru')
	article.save()

	from django.shortcuts import redirect
	return redirect (article)



'''