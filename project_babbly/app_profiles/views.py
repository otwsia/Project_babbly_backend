from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from administration.models import Account
from .models import Profile, FollowersCount
from app_posts.models import Post, Like, Reply
from .serializers import ProfileSerializer
from django.core import serializers
import json
from django.forms.models import model_to_dict
import random
from django.db.models import Q

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile


class Register(APIView):
    def put(self, request):
        #Save login details
        email = request.data['email']
        handle = request.data['handle']
        password = request.data['password']
        name = request.data['name']
        user = Account.objects.create_user(email=email, password=password, handle=handle, name=name)
        user.save()
        serialized_user = model_to_dict(user)
        #create profile
        user_model = Account.objects.get(email=email)
        new_profile = Profile.objects.create(user=user_model, handle=user_model.handle, name=user_model.name)
        new_profile.save()
        return Response(serialized_user)

class GetUser(APIView):
    def post(selfself, request):
        handle = request.data['handle']
        name = request.data['name']
        email = request.data['email']
        task = Account.objects.filter(Q(handle=handle) | Q(name=name) | Q(email=email))
        serialized_matches = json.loads(serializers.serialize('json', task))
        return Response(serialized_matches)

class ProfileUpdate(APIView):
    # permission_classes = (IsAuthenticated,)
    def patch(self, request):
        id = request.data['id']
        handle = request.data['handle']
        task = Profile.objects.get(user_id=id)
        serializer = ProfileSerializer(instance=task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        if 'profile_img' in request.data:
            regetTask = Profile.objects.filter(user_id=id).first()
            posts = Post.objects.filter(user=handle)
            if len(posts)>0:
                for post in posts:
                    post.profile_img = regetTask.profile_img
                    post.save()
            replies = Reply.objects.filter(user=handle)
            if len(replies)>0:
                for reply in replies:
                    reply.profile_img = regetTask.profile_img
                    reply.save()
        if 'name' in request.data:
            name = request.data['name']
            posts = Post.objects.filter(user=handle)
            if len(posts)>0:
                for post in posts:
                    post.name = name
                    post.save()
            replies = Reply.objects.filter(user=handle)
            if len(replies)>0:
                for reply in replies:
                    reply.name = name
                    reply.save()
        return Response(serializer.data)

class ProfileDelete(APIView):
    # permission_classes = (IsAuthenticated,)
    def delete(self, request):
        id = request.data['id']
        task = Account.objects.get(id=id)
        task.delete()
        return Response('Account deleted')
class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ImageFieldFile):
            return str(o)
        else:
            return super().default(o)
class GetProfile(APIView):
    # permission_classes = (IsAuthenticated,)
    def put(self, request, pk):
        user_profile = Profile.objects.get(handle=pk)
        serialized_profile = json.loads(serializers.serialize('json', [user_profile,]))[0]
        user_posts = Post.objects.filter(user=pk).order_by('-created_at')
        serialized_posts = json.loads(serializers.serialize('json', user_posts))
        for spost in serialized_posts:
            if spost['fields']['caption'] == None:
                og_post = Post.objects.get(id=spost['fields']['repost'])
                serialized_og_post = json.loads(serializers.serialize('json', [og_post, ]))[0]
                spost['fields']['caption'] = serialized_og_post
        user_posts_length = len(serialized_posts)

        follower = request.data['user']
        user = pk
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            button_text = 'Unfollow'
        else:
            button_text = 'Follow'
        user_followers = len(FollowersCount.objects.filter(user=pk))
        user_following = len(FollowersCount.objects.filter(follower=pk))

        liked_post_ids = []
        liked_post_data = []
        likes = Like.objects.filter(handle=user_profile)
        for posts in likes:
            liked_post_ids.append(posts.post_id)
        for ids in liked_post_ids:
            post_data = Post.objects.filter(id=ids)
            serialized_post_data = json.loads(serializers.serialize('json', post_data))
            if serialized_post_data != None:
                for posts in serialized_post_data:
                    liked_post_data.append(posts)

        task = Reply.objects.filter(user=pk).order_by('-created_at')
        serialized_task = json.loads(serializers.serialize('json', task))
        for replies in serialized_task:
            try:
                post = Post.objects.get(id=replies['fields']['post_id'])
            except:
                post = Reply.objects.get(id=replies['fields']['reply_id'])
            serialized_post = json.loads(serializers.serialize('json', [post, ]))[0]
            replies['fields']['og_post'] = serialized_post

        context = {
            'serialized_profile': serialized_profile,
            'serialized_posts': serialized_posts,
            'user_posts_length': user_posts_length,
            'button_text': button_text,
            'user_followers': user_followers,
            'user_following': user_following,
            'liked_post_data': liked_post_data,
            'replies_data': serialized_task
        }
        return Response(context)
        # return Response(1)

class Follow(APIView):
    # permission_classes = (IsAuthenticated,)
    def patch(self, request):
        follower = request.data['follower']
        user = request.data['user']
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return Response('Unfollowed')
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return Response('Followed')

class Suggest(APIView):
    # permission_classes = (IsAuthenticated,)
    def put(self, request):
        all_profiles = Profile.objects.all()
        all_followed_profiles = []
        followed_profile_handles = FollowersCount.objects.filter(follower=request.data['user'])
        for user in followed_profile_handles:
            profile_data = Profile.objects.get(handle=user.user)
            all_followed_profiles.append(profile_data)
        new_suggestion_list = [x for x in list(all_profiles) if (x not in list(all_followed_profiles))]
        user_profile = Profile.objects.filter(handle=request.data['user'])
        final_suggestions_list = [x for x in list(new_suggestion_list) if (x not in list(user_profile))]

        random.shuffle(final_suggestions_list)
        serialized_list = json.loads(serializers.serialize('json', final_suggestions_list))
        for profile in serialized_list:
            if profile['fields']['handle'] == "admin":
                serialized_list.remove(profile)
        return Response(serialized_list)

class Search(APIView):
    def get(self, request, pk, uk):
        profile_matches = Profile.objects.filter(Q(handle__icontains=pk) | Q(name__icontains=pk))
        serialized_profiles = json.loads(serializers.serialize('json', profile_matches))
        for profile in serialized_profiles:
            if profile['fields']['handle'] == "admin":
                serialized_profiles.remove(profile)
        for profile in serialized_profiles:
            if FollowersCount.objects.filter(follower=uk, user=profile['fields']['handle']).first():
                profile['fields']['button_text'] = 'Unfollow'
            else:
                profile['fields']['button_text'] = 'Follow'
        post_matches = Post.objects.filter(caption__icontains=pk)
        serialized_posts = json.loads(serializers.serialize('json', post_matches))
        res = {
            'serialized_profiles': serialized_profiles,
            'serialized_posts': serialized_posts
        }
        return Response(res)


