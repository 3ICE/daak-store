from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
import hello.views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^profile_developer/$', hello.views.profile_developer, name='profile_developer'),
    url(r'^profile_player/$', hello.views.profile_player, name='profile_player'),
    url(r'^signup/$', hello.views.signup, name='signup'),
    url(r'^add_game/$', hello.views.addgame, name='addgame'),
    url("^soc/", include("social_django.urls", namespace="social")),
    url(r'^games/(\w+)$', hello.views.game, name='game'),
    url(r'^games/$', hello.views.games, name='games'),
    url(r'^manage_game/$', hello.views.manage_game, name='manage_game'),
    url(r'^registration/$', hello.views.registration, name='registration'),
    url(r'^game_confirmation_delete/(.+)$', hello.views.game_confirmation_delete, name='game_confirmation_delete'),
    url(r'^user_verification/(.+)$', hello.views.user_verification, name='user_verification'),
    url(r'^update/(.+)$', hello.views.edit_game, name='update'),
    url(r'^pay_begin/(.+)$', hello.views.pay_begin, name='pay_begin'),
    url(r'^pay_success/.*', hello.views.pay_success),
    url(r'^pay_cancel/.*', hello.views.pay_cancel),
    url(r'^pay_failed/.*', hello.views.pay_failed),
]
