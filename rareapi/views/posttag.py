"""View module for handling requests about posttags"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import PostTag, Tag, Post

class PostTags(ViewSet):
    """Rare post tags"""

    def list(self, request):
        """Handle GET requests to get posttags by post"""

        posttags = PostTag.objects.all()

        #filtering posttags by post
        post = self.request.query_params.get("postId", None)

        if post is not None:
            posttags = posttags.filter(post_id=post)

        serializer = PostTagSerializer(
            posttags, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations"""

        post = Post.objects.get(pk=request.data["post_id"])
        tag = Tag.objects.get(pk=request.data["tag_id"])

        posttag = PostTag()
        posttag.post_id = post
        posttag.tag_id = tag

        try: 
            posttag.save()
            serializer = PostTagSerializer(posttag, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class PostTagSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for posttags
    Arguments:
        serializer type
    """

    class Meta:
        model = PostTag
        fields = ('id', 'post_id', 'tag_id')