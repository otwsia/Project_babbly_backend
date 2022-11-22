from rest_framework import serializers
from .models import Post, Reply

class PostSerializer(serializers.ModelSerializer):
    class Meta: # this is a keyword, used when creating a serializer for a table
        model = Post # tells you serializer has to be linked to Task table/model
        fields = '__all__' # to include all the fields

class ReplySerializer(serializers.ModelSerializer):
    class Meta: # this is a keyword, used when creating a serializer for a table
        model = Reply # tells you serializer has to be linked to Task table/model
        fields = '__all__' # to include all the fields