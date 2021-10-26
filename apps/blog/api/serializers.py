from rest_framework import serializers
from ..models import Article


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'title', 'category', 'slug', 'short_description', 'author', 'content', 'preview_image', 'likes', 'average_rating',
                  'is_recommended'
                  )


class ArticlePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'category', 'slug', 'short_description', 'content', 'preview_image')
