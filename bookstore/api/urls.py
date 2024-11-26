from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from .views import AuthorViewSet, BookViewSet

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title='Bookstore API',
        default_version='v1',
        description='API документация для работы с книгами и авторами',
    ),
    public=True,
)

v1_router = DefaultRouter()

v1_router.register('books', BookViewSet, basename='book')
v1_router.register('authors', AuthorViewSet, basename='author')

urlpatterns = [
    path('', include(v1_router.urls)),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
]
