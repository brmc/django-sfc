"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView


class T(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return {**kwargs, "list_a": [1,2,3], "list_b": [6,7,8]}


class O(TemplateView):
    template_name = 'other.html'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', T.as_view()),
    path('other/', O.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
