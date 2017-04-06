from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()

import hello.views

# Example:
# url(r'^blog/', include('blog.urls')),
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^signup/$', hello.views.signup, name='signup'),
]
