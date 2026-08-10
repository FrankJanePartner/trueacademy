"""
URL configuration for trueacademy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from contact.views import ContactMessageListCreateView, ContactMessageDetailView
from applications.views import ApplicationListCreateView, ApplicationDetailView
from gallery.views import GalleryImageListCreateView, GalleryImageDetailView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('index.html', TemplateView.as_view(template_name='index.html'), name='index'),
    path('about.html', TemplateView.as_view(template_name='about.html'), name='about'),
    path('cohort.html', TemplateView.as_view(template_name='cohort.html'), name='cohort'),
    path('gallery.html', TemplateView.as_view(template_name='gallery.html'), name='gallery'),
    path('contact.html', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('apply.html', TemplateView.as_view(template_name='apply.html'), name='apply'),
    path('admin/', admin.site.urls),
    path('api/contact/', ContactMessageListCreateView.as_view(), name='contact-list-create'),
    path('api/contact/<int:pk>/', ContactMessageDetailView.as_view(), name='contact-detail'),
    path('api/applications/', ApplicationListCreateView.as_view(), name='application-list-create'),
    path('api/applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('api/gallery/', GalleryImageListCreateView.as_view(), name='gallery-list-create'),
    path('api/gallery/<int:pk>/', GalleryImageDetailView.as_view(), name='gallery-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
