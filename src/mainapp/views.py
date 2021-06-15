from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from .serializers import *
from rest_framework import viewsets, generics, permissions, status
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        serializer = UserSerialiserWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SignUp(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        password2 = data['password2']
        if not password==password2:
            message = {'detail':'Ошибка: Пароли не совпадают'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            if User.objects.filter(username=username).exists():
                message = {'detail':'Ошибка: Пользователь с таким логином уже существует'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                new_user = User.objects.create_user(
                    username=username,
                    password=password
                    )
            serialiser = UserSerialiserWithToken(new_user, many=False)
        return Response(serialiser.data)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-date')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_post(request, id):
    post = Post.objects.get(id=id)
    serializer = PostSerializer(post)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_post(request):
    data = request.data
    post_id=data.get('id')
    post = Post.objects.get(id=post_id)
    post.name = data.get('name')
    post.text = data.get('text')
    post_check = Post.objects.filter(user=request.user, name=data.get('name'))
    print()
    if post_check.exists():
        if int(post_check[0].id) != int(post_id):
            message = {'detail': 'Пост с таким названием уже существует'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        post.save()
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)
    else:
        post.save()
        serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, id):
    try:
        Post.objects.get(id=id).delete()
    except:
        return Response('Post has not been updated', status=status.HTTP_400_BAD_REQUEST)
    return Response('Post has been deleted', status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    user = request.user
    post_name = request.data.get('name')
    post_text = request.data.get('text')
    if post_name and post_text:
        if Post.objects.filter(user=user, name=post_name):
            message= {'detail':'Пост с таким названием уже существует'}
            return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            new_post = Post.objects.create(
                user=user,
                name=post_name,
                text=post_text
            )
    else:
        return Response('Post has not been created', status=status.HTTP_400_BAD_REQUEST)
    serialiser = PostSerializer(new_post, many=False)
    return Response(serialiser.data)


