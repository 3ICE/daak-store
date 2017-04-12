from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()

import hello.views

# Example:
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^profile_developer/$', hello.views.profile_developer, name='profile_developer'),
    url(r'^signup/$', hello.views.signup, name='signup'),
    url(r'^add_game/$', hello.views.addgame, name='addgame'),
    url("^soc/", include("social_django.urls", namespace="social"))
]
