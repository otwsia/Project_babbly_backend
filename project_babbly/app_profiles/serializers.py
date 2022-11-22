from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta: # this is a keyword, used when creating a serializer for a table
        model = Profile # tells you serializer has to be linked to Task table/model
        fields = '__all__' # to include all the fields