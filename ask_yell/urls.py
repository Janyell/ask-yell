from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover().

urlpatterns = patterns('',
    url(r'^$', 'ask.views.question_list', {'sort': 'new'}, name='index'),
    url(r'^new/$', 'ask.views.question_list', {'sort': 'new'}, name='new'),
    url(r'^popular/$', 'ask.views.question_list', {'sort': 'popular'}, name='popular'),
    url(r'^question/(?P<question_pk>\d+)/$', 'ask.views.question_detail', name='answer'),
    url(r'^author/(?P<author_pk>\d+)/$', 'ask.views.question_list', name='author_question'),
    url(r'^author/(?P<author_pk>\d+)/questions/$', 'ask.views.question_list', name='author_question'),
    url(r'^author/(?P<author_pk>\d+)/answers/$', 'ask.views.answer_list', name='author_answer'),
    url(r'^registration/$', 'ask.views.registration', name='registration'),
    url(r'^login/$', 'ask.views.log_in', name='login'),
    url(r'^logout/$', 'ask.views.log_out', name='logout'),  
    url(r'^right-answer/(?P<answer_pk>\d+)/$', 'ask.views.right_answer', name='right_answer'),
    url(r'', 'ask.views.page_not_found', name='404'),
    #url(r'^like-question/(?P<question_pk>\d+)/$', 'ask.views.like_question', name='like_question'),
    #url(r'^dislike-question/(?P<question_pk>\d+)/$', 'ask.views.dislike_question', name='like_question'),
    #url(r'^like-answer/(?P<answer_pk>\d+)/$', 'ask.views.like_answer', name='like_answer'),
    #url(r'^dislike-answer/(?P<answer_pk>\d+)/$', 'ask.views.dislike_answer', name='dislike_answer'), 
    # Examples:
    # url(r'^$', 'ask_yell.views.home', name='home'),
    # url(r'^ask_yell/', include('ask_yell.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
