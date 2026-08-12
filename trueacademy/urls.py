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
from django.urls import path, re_path
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.static import serve
from trueacademy.views import csrf_bootstrap
from contact.views import ContactMessageListCreateView, ContactMessageDetailView
from applications.views import ApplicationListCreateView, ApplicationDetailView
from gallery.views import GalleryImageListCreateView, GalleryImageDetailView, GalleryCategoryListView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('index', TemplateView.as_view(template_name='index.html'), name='index'),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('cohort', TemplateView.as_view(template_name='cohort.html'), name='cohort'),
    path('gallery', TemplateView.as_view(template_name='gallery.html'), name='gallery'),
    path('contact', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('apply', TemplateView.as_view(template_name='apply.html'), name='apply'),
    path('admin/', admin.site.urls),
    path('api/csrf/', csrf_bootstrap, name='csrf-bootstrap'),
    re_path(r'^api/contact/?$', ContactMessageListCreateView.as_view(), name='contact-list-create'),
    path('api/contact/<int:pk>/', ContactMessageDetailView.as_view(), name='contact-detail'),
    re_path(r'^api/applications/?$', ApplicationListCreateView.as_view(), name='application-list-create'),
    path('api/applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),

    path('api/gallery/categories/', GalleryCategoryListView.as_view(), name='gallery-categories'),
    path('api/gallery/', GalleryImageListCreateView.as_view(), name='gallery-list-create'),
    path('api/gallery/<int:pk>/', GalleryImageDetailView.as_view(), name='gallery-detail'),

    # Existing template links remain valid while the routes above stay canonical.
    path('index', RedirectView.as_view(pattern_name='index', permanent=False)),
    path('about', RedirectView.as_view(pattern_name='about', permanent=False)),
    path('cohort', RedirectView.as_view(pattern_name='cohort', permanent=False)),
    path('gallery', RedirectView.as_view(pattern_name='gallery', permanent=False)),
    path('contact', RedirectView.as_view(pattern_name='contact', permanent=False)),
    path('apply', RedirectView.as_view(pattern_name='apply', permanent=False)),

    # WhiteNoise serves static assets but not files uploaded through Django admin.
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
