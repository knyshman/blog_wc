from django.contrib.auth import get_user_model
from django.test import TestCase
from apps.blog.models import Article, Category

User = get_user_model()


class ArticleModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.category1 = Category.objects.create(name='category1',
                                                 slug='category-1',
                                                 depth=1,
                                                 path='001'
                             )
        self.category2 = Category.objects.create(name='category2',
                                                 slug='category-2',
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
    #
    # def test_first_name_label(self):
    #     author = Author.objects.get(id=1)
    #     field_label = author._meta.get_field('first_name').verbose_name
    #     self.assertEquals(field_label, 'first name')
    #
    # def test_date_of_death_label(self):
    #     author=Author.objects.get(id=1)
    #     field_label = author._meta.get_field('date_of_death').verbose_name
    #     self.assertEquals(field_label,'died')
    #
    # def test_first_name_max_length(self):
    #     author=Author.objects.get(id=1)
    #     max_length = author._meta.get_field('first_name').max_length
    #     self.assertEquals(max_length,100)

    def test_get_absolute_url(self):
        article=Article.objects.get(slug='article-2')
        self.assertEquals(article.get_absolute_url(), '/ru/blog/article-2/')