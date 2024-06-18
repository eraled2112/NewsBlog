from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import News
from .serializers import NewsSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated


class NewsListApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):
        todos = News.objects.filter(user=request.user.id)
        serializer = NewsSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'created_at': request.data.get('created_at'),
            'user': request.user.id
        }
        serializer = NewsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewsDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, news_id, user_id):
        try:
            return News.objects.get(id=news_id, user = user_id)
        except News.DoesNotExist:
            return None

    def get(self, request, news_id, *args, **kwargs):
        news_instance = self.get_object(news_id, request.user.id)
        if not news_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = NewsSerializer(news_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, news_id, *args, **kwargs):
        news_instance = self.get_object(news_id, request.user.id)
        if not news_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'created_at': request.data.get('created_at'),
            'user': request.user.id
        }
        serializer = NewsSerializer(instance = news_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, news_id, *args, **kwargs):
        news_instance = self.get_object(news_id, request.user.id)
        if not news_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        news_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
