from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from random import randint
from .utils.sorting import Sorting

class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        q_params = request.query_params.get('filter[title][$in]', None)
        serializer = PostSerializer(posts, many=True)
        filtered_data = []
        # fileter by title
        if q_params:
            for post in serializer.data:
                if post['title'] in q_params:
                    filtered_data.append(post)
        else:
            filtered_data = serializer.data

        # sort by date
        sorted_data = Sorting.sort_by_date(filtered_data)
        print(sorted_data)

        # create response
        return Response({
            "data": sorted_data,
            "meta": {
                "total": len(serializer.data)
            },
            "success": True
        }, status=status.HTTP_200_OK)

    def post(self, request):
        payload = request.data["data"]
        payload['document_id'] = randint(0, 1000000)
        serializer = PostSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "meta": {},
                "success": True
            }, status=status.HTTP_201_CREATED)
        return Response({
            "data": None,
            "meta": {},
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response({
            "data": serializer.data,
            "meta": {},
            "success": True
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Retrieve the post from the database using the primary key
        post = Post.objects.get(pk=pk)

        # TODO: fix issue with required fields
        # This comment suggests there's an issue with handling required fields, which might lead to validation errors

        # Serialize the post with new data from the request
        serializer = PostSerializer(post, data=request.data["data"])

        # Check if the serializer data is valid
        if serializer.is_valid():
            # If valid, save the changes
            serializer.save()
            return Response({
                "data": serializer.data,
                "meta": {},
                "success": True
            }, status=status.HTTP_200_OK)
        else:
            # If not valid, return the errors
            return Response({
                "data": None,
                "meta": {},
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response({
            "data": None,
            "meta": {},
            "success": True
        }, status=status.HTTP_204_NO_CONTENT)

# Create your views here.
