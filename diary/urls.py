from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include('users.urls')),
    path('',include('cases.urls')),
    path('',include('accounts.urls')),
    path('',include('frontpage.urls')),
    path('admin/', admin.site.urls),
    # path('',include('django.contrib.auth.urls')),
    path('tinymce/', include('tinymce.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = 'users.views.custom_404'
