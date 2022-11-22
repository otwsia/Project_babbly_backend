from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.response import Response
from rest_framework.views import APIView
from app_profiles.models import Profile, FollowersCount
from .models import Post, Reply, Like
from .serializers import PostSerializer, ReplySerializer
from django.forms.models import model_to_dict
from django.core import serializers
import json
from django.http import JsonResponse

class Upload(APIView):
    # permission_classes = (IsAuthenticated,)
    def put(self, request):
        user = request.data['user']
        user_model = Profile.objects.get(handle=user)
        request.data._mutable = True
        request.data['user_id'] = user_model.id_user
        serializer = PostSerializer(
            data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_model.no_of_posts = user_model.no_of_posts + 1
            user_model.save()
            return Response({'posted': serializer.data})
        else:
            return Response(serializer.errors)

class Delete(APIView):
    # permission_classes = (IsAuthenticated,)
    def delete(self, request):
        id = request.data['id']
        task = Post.objects.get(id=id)
        user = task.user
        user_model = Profile.objects.get(handle=user)
        user_model.no_of_posts = user_model.no_of_posts - 1
        user_model.save()
        task.delete()
        return Response('Post deleted')

class ReplyUpload(APIView):
    # permission_classes = (IsAuthenticated,)
    def put(self, request, pk):
        user = request.data['user']
        request.data._mutable = True
        user_model = Profile.objects.get(handle=user)
        try:
            post_model = Post.objects.filter(id=pk).first()
            post_model.no_of_replies = post_model.no_of_replies + 1
            post_model.save()
            request.data['post_id'] = post_model.id
        except:
            reply_model = Reply.objects.filter(id=pk).first()
            reply_model.no_of_replies = reply_model.no_of_replies + 1
            reply_model.save()
            request.data['reply_id'] = reply_model.id

        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            user_model.no_of_posts = user_model.no_of_posts + 1
            user_model.save()
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class ReplyDelete(APIView):
    # permission_classes = (IsAuthenticated,)
    def delete(self, request):
        id = request.data['id']
        task = Reply.objects.get(id=id)
        user = task.user
        user_model = Profile.objects.get(handle=user)
        user_model.no_of_posts = user_model.no_of_posts - 1
        user_model.save()
        task.delete()
        return Response('Reply deleted')

class GetReply(APIView):
    # permission_classes = (IsAuthenticated,)
    def put(self, request):
        user = request.data['user']
        task = Reply.objects.filter(user=user).order_by('-created_at')
        serialized_task = json.loads(serializers.serialize('json', task))
        for replies in serialized_task:
            try:
                post = Post.objects.get(id=replies['fields']['post_id'])
            except:
                post = Reply.objects.get(id=replies['fields']['reply_id'])
            serialized_post = json.loads(serializers.serialize('json', [post, ]))[0]
            replies['fields']['og_post'] = serialized_post
        return Response(serialized_task)

class GetRepList(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, pk):
        task = Reply.objects.filter(post_id=pk).order_by('-created_at')
        serialized_task = json.loads(serializers.serialize('json', task))
        return Response(serialized_task)

class PostList(APIView):
    def put(self, request):
        if request.data['user'] != "None":
            follower = request.data['user']
            user_following_list = []
            feed = []
            user_following = FollowersCount.objects.filter(follower=follower)
            for users in user_following:
                user_following_list.append(users.user)
            user_following_list.append(follower)
            for usernames in user_following_list:
                feed_list = Post.objects.filter(user=usernames)
                serialized_feed_list = json.loads(serializers.serialize('json', feed_list))
                if serialized_feed_list != None:
                    for posts in serialized_feed_list:
                        feed.append(posts)
            newFeed = sorted(feed, key=lambda d: d['fields']['created_at'], reverse=True)
            for spost in newFeed:
                if spost['fields']['caption'] == None:
                    og_post = Post.objects.get(id=spost['fields']['repost'])
                    serialized_og_post = json.loads(serializers.serialize('json', [og_post, ]))[0]
                    spost['fields']['caption']=serialized_og_post
            return Response(newFeed)
        else:
            tasks = Post.objects.all().order_by('-created_at')
            serialized_feed_list = json.loads(serializers.serialize('json', tasks))
            for spost in serialized_feed_list:
                if spost['fields']['caption'] == None:
                    og_post = Post.objects.get(id=spost['fields']['repost'])
                    serialized_og_post = json.loads(serializers.serialize('json', [og_post, ]))[0]
                    spost['fields']['caption']=serialized_og_post
            return Response(serialized_feed_list)
class Liked(APIView):
    # permission_classes = (IsAuthenticated,)
    def patch(self, request):
        handle = request.data['handle']
        post_id = request.data['post_id']
        try:
            post = Post.objects.get(id=post_id)
        except:
            post = Reply.objects.get(id=post_id)
        liked_post = Like.objects.filter(post_id=post_id, handle=handle).first()
        if liked_post == None:
            new_like = Like.objects.create(post_id=post_id, handle=handle)
            new_like.save()
            post.no_of_likes=post.no_of_likes+1
            post.save()
            return Response('Liked')
        else:
            liked_post.delete()
            post.no_of_likes = post.no_of_likes-1
            post.save()
            return Response('Unliked')

class Reposted(APIView):
    def patch(self, request):
        user = request.data['handle']
        name = request.data['name']
        post_id = request.data['post_id']

        user_model = Profile.objects.get(handle=user)
        post = Post.objects.get(id=post_id)
        existing_repost = Post.objects.filter(repost=post).first()
        if existing_repost == None:
            new_post = Post.objects.create(user_id=user_model, user=user, name=name, repost=post)
            new_post.save()
            post.no_of_reposts = post.no_of_reposts + 1
            post.save()
            user_model.no_of_posts = user_model.no_of_posts + 1
            user_model.save()
            return Response('Reposted')
        else:
            existing_repost.delete()
            post.no_of_reposts = post.no_of_reposts - 1
            post.save()
            user_model.no_of_posts = user_model.no_of_posts - 1
            user_model.save()
            return Response('Unreposted')
