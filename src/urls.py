from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from main.views import IndexView, StudentView, RegistrationView, AddStudentView, AddGroupView, ManageStudentView, ManageGroupView
import settings

urlpatterns = patterns('',
    url(r'^registration/$', RegistrationView.as_view()),
    url(r'^student/add/$', AddStudentView.as_view()),
    url(r'^student/manage/(?P<pk>\d+)/$', ManageStudentView.as_view()),
    url(r'^group/add/$', AddGroupView.as_view()),
    url(r'^group/manage/(?P<pk>\d+)/$', ManageGroupView.as_view()),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'user/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/login/'}),
    url(r'^accounts/profile/', 'django.views.generic.simple.redirect_to', {'url': '/'}),
    url(r'^group/(?P<pk>\d+)/$', StudentView.as_view()),
    url(r'^group/(?P<pk>\d+)/page(?P<page>\d+)/$', StudentView.as_view()),
    url(r'^$', IndexView.as_view()),
)

urlpatterns += patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^content/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes':True
    }),
)
