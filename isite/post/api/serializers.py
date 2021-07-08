from rest_framework import serializers
from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')


    class Meta:
        model = Post
        fields = ['id', 'username', 'title', 'content', 'publishing_date', 'image', 'topic', 'slug']


    def get_username_from_author(self, post):
        username = post.user.username
        return username
