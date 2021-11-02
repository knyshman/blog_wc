from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.text import slugify
from apps.blog.models import Article, Category, ArticleRating
from apps.blog.utils import from_cyrillic_to_eng

User = get_user_model()


class ArticleModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.category1 = Category.objects.create(name='category 1',
                                                 slug='category_1',
                                                 depth=1,
                                                 path='001'
                             )
        self.category2 = Category.objects.create(name='category2',
                                                 slug='category2',
                                                 depth=1,
                                                 path='002'
                             )
        lst = [Article(title='article1',
                          slug='article-1',
                          author=User.objects.first(),
                          short_description='short_description1',
                          content='content1',
                          category=self.category1,

                          ),
        Article(title='article2',
                          slug='article-2',
                          author=User.objects.first(),
                          short_description='short_description2',
                          content='content2',
                          category=self.category2,
                          )
        ]
        Article.objects.bulk_create(lst)

    def test_category_str_title(self):
        self.assertEquals(self.category1.__str__(), self.category1.name)

    def test_category_slug(self):
        self.assertEquals(self.category1.slug, slugify(from_cyrillic_to_eng(self.category1.name)))

    def test_article_label(self):
        article = Article.objects.get(id=1)
        field_label = article._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_str_title(self):
        article = Article.objects.get(id=1)
        self.assertEquals(article.__str__(), article.title)

    def test_get_absolute_url(self):
        article = Article.objects.get(slug='article-2')
        self.assertEquals(article.get_absolute_url(), '/ru/blog/article-2/')


