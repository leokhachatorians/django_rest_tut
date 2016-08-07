from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'pk', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')

    def create(self, validated_data):
        """
        Create and return a 'Snippet' instance
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail',
                                                   read_only=True)

    class Meta:
        model = User
        fields = ('url', 'pk', 'username', 'snippets', 'password', 'email')
        write_only_fields = {'password'}

    def create(self, validated_data):
        u = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
        )

        u.set_password(validated_data['password'])
        u.save()
        return u
