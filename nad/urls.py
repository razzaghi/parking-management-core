from django.conf.urls import url, include
from django.contrib import admin
from nad_app import views
from rest_framework_jwt.views import obtain_jwt_token
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                  url(r'^admin/', admin.site.urls),  # for django admin.
                  # url(r'', include('nad_app.urls'), name='nad_app'),
                  url(r'', include('Users.urls'), name='Users'),
                  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
                  # url(r'graphql', GraphQLView.as_view(graphiql=True) ),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
