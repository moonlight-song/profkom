from os.path import join as path_join
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File as DjangoFile
from django.views import View
from django.template.response import TemplateResponse
from django.utils import translation

from aldryn_people.models import Person
from django.utils.safestring import SafeText
from aldryn_newsblog.models import Article
from aldryn_newsblog.cms_appconfig import NewsBlogConfig
from aldryn_newsblog.views import ArticleListBase
from aldryn_categories.models import Category
from filer.management.commands.import_files import FileImporter
from cms.api import add_plugin
from cms.models.placeholdermodel import Placeholder
from cms.apphook_pool import apphook_pool

class IndexView (ArticleListBase) :

	show_header = True
	template_name = "aldryn_newsblog/frontpage.html"


	def get_queryset(self):
		
		return Article.objects.language('ru').all()[2:]


	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['pagination'] = self.get_pagination_options()
		context['slider_articles'] = Article.objects.language('ru').all()[0:2]
		context['featured_articles'] = Article.objects.language('ru').filter(is_featured = True) \
			.order_by('-publishing_date')[:4]
		context['row_markers'] = [Article.objects.language('ru').filter(is_featured = True)[:4]]
		return context
	

VK_URL_TEMPLATE = "https://api.vk.com/method/{method_name}?{parameters}&access_token={access_token}&v={api_version}"


def retrieveAcessToken():
	return "6160b92c6160b92c6160b92c9261053238661606160b92c3a0916672b1e9ddd8d1fc1ed"

def truncateSymbols(text, num_symbols):
	if len (text) <= num_symbols:
		return text
	else:
		result = text[0:num_symbols]
		return result[0:result.rfind (' ')] + " ..."	


def checkVkPosts(request):
	
	url = VK_URL_TEMPLATE.format (method_name = "wall.get", api_version = "5.60", parameters = "domain=profkom_phystech",
		access_token = retrieveAcessToken())
	response = requests.get(url)
	#r.status_code
	response_data = response.json()
	
	posts = response_data['response']['items']
	posts_to_load = []

	for post in posts :
		#return HttpResponse (len(post['copy_history']) != 0)
		if 'copy_history' in post : continue
		#if postAlreadyLoaded(post['post_id']) : continue
		posts_to_load.append(post)

	article = None
	for post in posts_to_load : article = importVkPost (post)
	return redirect (article)


def getCategoryByHashtag (article_text) :

	category_name = article_text[article_text.rfind('#')+1:article_text.rfind('@')].upper()
	
	try : 
		category = Category.objects.language('ru').filter(translations__name = category_name)
	except aldryn_categories.models.DoesNotExist :
		category = Category.objects.language('ru').filter(translations__name = category_name)
		article.set_current_language('ru')
		# lft - дерево категорий
		article.save()

def importVkPost (post):

	title = truncateSymbols(post['text'], 50)

	try :
		attachment = post['attachments'][0]
		photo_key = ""
		for key in attachment['photo'] : 
			if 'photo_' in key : photo_key = key
		pic_url = attachment['photo'][photo_key]

		# Check whether it is a picture
		header = requests.head(pic_url, allow_redirects=True)
		if 'image' not in header.headers.get('content-type').lower() :
			raise Exception()

		pic_response = requests.get(pic_url, allow_redirects=True)
		url_end_index = pic_url.find('.com')
		path_to_save = pic_url[url_end_index + 5 : ].replace('/', '_')
		
		pic_file = open(path_join(settings.MEDIA_ROOT, 'vk_pictures', path_to_save), 'w+b')
		pic_file.write(pic_response.content)
		pic_file.seek(0)

		importer = FileImporter()
		folder = FileImporter.get_or_create_folder(importer, ['base', 'subfolder'])
		file_obj = DjangoFile(pic_file, name = title +'.jpg')
		pic = importer.import_file(file_obj, folder)
		pic.save()
		pic_file.close()

	except KeyError : 
		pic = None
		pass

	except :
		pic = None
		raise

	lead_in = SafeText(truncateSymbols(post['text'], 300))


	try:
		user = User.objects.get(username = 'vk')
	except django.contrib.auth.models.DoesNotExist:
		raise Exception ("Должен быть создан пользователь с именем 'vk'")
	try:
		author = Person.objects.language('ru').get (user = user)
	except django.contrib.auth.models.DoesNotExist:
		raise Exception ("Должен быть создан Aldryn NewsBlog человек со ссылкой на пользователя 'vk'")
	
	try:
		config = NewsBlogConfig.objects.language('ru').all()[0]
	except IndexError:
		raise Exception ("No available NewsBlog config!")

	article = Article(author = author, app_config = config, owner = user, 
		title = title, featured_image = pic, lead_in = lead_in, is_published = True)
	article.set_current_language('ru')
	article.save()

	placeholder = article.content
	add_plugin(placeholder, 'TextPlugin', 'ru', body = post['text'])

	return article

#происшествия@profkom_phystech

def convert_hashtag_to_category (article):

	if len(article.categories.all()) > 0 : return

	plugin = article.content.get_plugins().filter(plugin_type='TextPlugin')[0]
	text = plugin.get_plugin_instance()[0]
	index_at = text.body.find('@profkom_phystech')

	if (index_at == -1 ) : 
		print ('Article {} : hashtag not found'.format(article))
		return

	index_sharp = text.body[:index_at].rfind('#')	
	category_name = text.body[index_sharp+1 : index_at].capitalize()
	text.body = text.body[:index_sharp]
	text.save()

	translation.activate('ru')

	root = Category.objects.all()[0].get_root()
	candidate_categories = [[item.name, item.id] for item in root.get_children() 
		if category_name in item.name] 

	if len(candidate_categories) > 0 :
		category = Category.objects.get(id = candidate_categories[0][1])
	else :
		category = root.add_child(name = category_name)

	article.categories.add(category)
	article.save()






