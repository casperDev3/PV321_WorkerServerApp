
from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/feed/', include('Feed.urls')),
    path('api/v1/notifications', include('Notifications.urls')),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]
