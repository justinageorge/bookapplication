from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets

from rest_framework.response import Response
from book.models import Books
from api.serializers import BookSerializer


class BookListCreateView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Books.objects.all()
        serializer=BookSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def post(self,request,*args,**kwargs):
        serializer=BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:

            return Response(data=serializer.errors)
    
class BookUpdateDetailDestroyView(APIView):
    def get(self,request,*args,**kwargs): 
        id=kwargs.get("pk")
        qs=Books.objects.get(id=id)
        serializer=BookSerializer(qs)
        return Response(data=serializer.data)
    
    def put(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        book_object=Books.objects.get(id=id)
        serializer=BookSerializer(data=request.data,instance=book_object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:

            return Response(data=serializer.errors)
    
    def delete(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Books.objects.get(id=id).delete()
        return Response(data={"message":"book deleted"})


class BookViewSetView(viewsets.ViewSet):
    def list(self,request,*args,**kwargs):
        qs=Books.objects.all()
        serializer=BookSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Books.objects.get(id=id)
        serializer=BookSerializer(data=qs)
        return Response(data=serializer.data)
    
    def create(self,request,*args,**kwargs):
        serializer=BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        book_object=Books.objects.get(id=id)
        serializer=BookSerializer(data=request.data,instance=book_object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

        

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Books.objects.get(id=id).delete()
        return Response(data={"message":"book deleted"})