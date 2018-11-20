from os.path import join as path_join
import requests
from datetime import datetime

from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File as DjangoFile
from django.utils import translation

from aldryn_people.models import Person
from django.utils.safestring import SafeText
from aldryn_newsblog.cms_appconfig import NewsBlogConfig
from aldryn_newsblog.models import Article
from aldryn_categories.models import Category
from filer.management.commands.import_files import FileImporter
from cms.api import add_plugin
from cms.models.placeholdermodel import Placeholder
from cms.apphook_pool import apphook_pool

from .models import VkPost


class VkPostsImporter(object):

	api_url_template = "https://api.vk.com/method/{method_name}?{parameters}&access_token={access_token}&v={api_version}"
	access_token = "6160b92c6160b92c6160b92c9261053238661606160b92c3a0916672b1e9ddd8d1fc1ed"

	
	def __init__(self):

		url = self.api_url_template.format (method_name = "wall.get", api_version = "5.60", parameters = "domain=profkom_phystech",
			access_token = self.access_token)
		response = requests.get(url)
		response_data = response.json()
		
		import json
		
		if 'error' in response_data :
			self.valid_data_from_vk = False
			print (json.dumps(response_data, indent = 1))
		else :
			self.valid_data_from_vk = True
			self.response_data = response_data['response']


	def retrieve_missing_posts(self):
		
		if self.valid_data_from_vk :

			missing_posts_tuples = self.check_missing_posts()
			if missing_posts_tuples :
				for post_tuple in missing_posts_tuples : self.download_post (post_tuple)

		else :
			print ('Invalid data from vk')


	def reload_all_posts(self):

		if self.valid_data_from_vk :

			translation.activate('ru')
			vk_person = Person.objects.filter(user__username = settings.VK_USER_USERNAME)
			vk_articles = Article.objects.filter(author = vk_person)
			for article in vk_articles : article.delete()

			vk_posts = VkPost.objects.all()
			for post in vk_posts : post.delete()

			missing_posts_tuples = self.check_missing_posts()
			if missing_posts_tuples :
				for post_tuple in missing_posts_tuples : self.download_post (post_tuple)

		else :
			print ('Invalid data from vk')
		

	def check_missing_posts(self):
		
		posts = self.response_data['items']
		posts_to_load = []
		loaded_posts_ids = [post.post_id for post in VkPost.objects.all()]
		#print ("Loaded_posts_ids : {}".format(loaded_posts_ids))

		for post in posts :
			if post['id'] in loaded_posts_ids : continue # post with this id is already loaded
			if 'copy_history' in post : continue # it's a repost from other public page, skip it
			#print ("Post id {} is to be loaded".format(post['id']))
			
			post_photo_key = self.get_post_photo_key(post)
			if post_photo_key: 
				posts_to_load.append((post, post_photo_key))
			else:
				continue

		return posts_to_load


	def get_post_photo_key(self, post):
		"""
		Returns index of photo in json in case the good one was found 
		and False otherwise
		"""
		if 'photo' not in post['attachments'][0]: return False
			
		filtered = list(filter(lambda x: "photo_" in x, post['attachments'][0]['photo']))
		if len(filtered) == 0 : return False

		photo_size = max([int(item[6:]) for item in filtered])
		return "photo_{}".format(photo_size) if photo_size >= 360 else False
		"""
		attachment = post['attachments'][0]
		photo_key = ""
		photo_size = 0

		for key in attachment['photo'] : 
			if 'photo_' in key : 
				current_photo_size = int(key[6:])
				if current_photo_size > photo_size : 
					photo_size = current_photo_size
					photo_key = key

		if photo_key != "" and int(photo_key) > 360 :
			return "photo_" + photo_key
		else:
			return False
		"""
		

	def download_post(self, post_tuple):

		post = post_tuple[0]
		photo_key = post_tuple[1]

		translation.activate('ru')
		print ("Post {} is being downloaded".format(post['id']))

		title = self.truncate_text_to_title(post['text'], 50)

		try :
			attachment = post['attachments'][0]

			pic_url = attachment['photo'][photo_key]

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

		lead_in = SafeText(self.truncate_text_to_title(post['text'], 300))


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

		publishing_date = datetime.fromtimestamp(int(post['date']))

		article = Article(author = author, app_config = config, owner = user, title = title, 
			publishing_date = publishing_date, featured_image = pic, lead_in = lead_in, is_published = True)
		article.set_current_language('ru')
		article.save()

		placeholder = article.content
		add_plugin(placeholder, 'TextPlugin', 'ru', body = post['text'])
		self.convert_hashtag_to_category(article)

		VkPost.objects.create(post_id = post['id'], date = post['date'], article = article)

		return article


	def truncate_text_to_title(self, text, num_symbols):
		if len (text) <= num_symbols:
			return text
		else:
			result = text[0:num_symbols]
			return result[0:result.rfind (' ')] + " ..."	


	def convert_hashtag_to_category(self, article):

		if len(article.categories.all()) > 0 : return

		plugin = article.content.get_plugins().filter(plugin_type='TextPlugin')[0]
		text = plugin.get_plugin_instance()[0]
		index_at = text.body.rfind('@')

		if (index_at == -1 ): 
			print ('Article {} : hashtag not found'.format(article))
			return

		index_sharp = text.body[:index_at].rfind('#')	
		category_name = text.body[index_sharp+1 : index_at].capitalize().replace('_', ' ')
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
