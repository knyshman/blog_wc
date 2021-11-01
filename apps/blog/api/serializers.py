from django.contrib.auth import get_user_model
from rest_framework import serializers


from ..models import Article, Image, Like

User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', 'alt')


class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', 'alt', 'article')


class ArticleSerializer(serializers.ModelSerializer):
    image_set = ImageSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'category', 'slug', 'short_description', 'author', 'content', 'preview_image', 'likes', 'average_rating',
                  'is_recommended', 'image_set'
                  )


class ArticlePostSerializer(serializers.ModelSerializer):
    image_set = ImagePostSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'category', 'slug', 'short_description', 'content', 'preview_image', 'image_set')

    def create(self, validated_data):
        image_set = validated_data.pop('image_set')
        article = super().create(validated_data)
        for child in image_set:
            child['article'] = article
        self.fields['image_set'].create(image_set)
        return article


class SubscribesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'last_name', 'phone', 'subscribes')
        read_only_fields = ('email', 'name', 'last_name', 'phone', 'subscribes')



class ProfileSerializer(serializers.ModelSerializer):
    subscribes = SubscribesSerializer(many=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'last_name', 'phone', 'is_active', 'is_superuser', 'avatar', 'subscribes', 'user_permissions', 'password')
        read_only_fields = ('is_active', 'email', 'is_superuser', 'user_permissions', 'subscribes')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('article', 'like', 'user')
        read_only_fields = ('like', 'user', 'article')
