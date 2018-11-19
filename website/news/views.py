from aldryn_newsblog.models import Article
from aldryn_newsblog.views import ArticleListBase


class IndexView (ArticleListBase) :

	show_header = True
	template_name = "aldryn_newsblog/frontpage.html"


	def get_queryset(self):

		return Article.objects.language('ru').all().order_by('-vkpost__date')[2:]


	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['pagination'] = self.get_pagination_options()
		context['slider_articles'] = Article.objects.language('ru').all().order_by('-vkpost__date')[0:2]
		context['featured_articles'] = Article.objects.language('ru').filter(is_featured = True) \
			.order_by('-vkpost__date')[:4]
		#context['row_markers'] = [Article.objects.language('ru').filter(is_featured = True)[:4]]
		return context
