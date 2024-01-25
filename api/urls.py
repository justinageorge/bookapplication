from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("v1/books",views.BookViewSetView,basename="books")
  


urlpatterns=[
    path("books/",views.BookListCreateView.as_view()),
    path("books/<int:pk>/",views.BookUpdateDetailDestroyView.as_view()),

]+router.urls