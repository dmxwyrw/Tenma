from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from comics.views import SeriesList, SeriesDetail, IssueDetail, CharacterDetail, ArcDetail, \
    TeamDetail, PublisherDetail, CreatorDetail, IssueUpdateView, IssueDeleteView, \
    ServerSettingsView, read, importer, reprocess, update_issue_status, SearchSeriesList

app_name = 'comics'
urlpatterns = [
    url(r'^series/$',
        SeriesList.as_view(),
        name='series-list'),
    url(r'^search/?$',
        SearchSeriesList.as_view(),
        name='series_search_list'),
    url(r'^series/(?P<slug>[\w\-]+)/$',
        SeriesDetail.as_view(),
        name='series-detail'),
    url(r'^issue/(?P<slug>[\w\-]+)/$',
        IssueDetail.as_view(),
        name='issue-detail'),
    url(r'^issue/(?P<slug>[\w\-]+)/read$',
        read,
        name='read'),
    url(r'^issue/(?P<slug>[\w\-]+)/update-status$',
        update_issue_status,
        name='update_issue_status'),
    url(r'^character/(?P<slug>[\w\-]+)/$',
        CharacterDetail.as_view(), name='character-detail'),
    url(r'^arc/(?P<slug>[\w\-]+)/$',
        ArcDetail.as_view(),
        name='arc-detail'),
    url(r'^team/(?P<slug>[\w\-]+)/$', TeamDetail.as_view(), name='team-detail'),
    url(r'^publisher/(?P<slug>[\w\-]+)/$',
        PublisherDetail.as_view(), name='publisher-detail'),
    url(r'^creator/(?P<slug>[\w\-]+)/$',
        CreatorDetail.as_view(),
        name='creator-detail'),
    url('importer', importer, name='importer'),
    url(r'^issue/(?P<slug>[\w\-]+)/update/$',
        IssueUpdateView.as_view(), name='issue-update'),
    url(r'^issue/(?P<slug>[\w\-]+)/delete/$',
        IssueDeleteView.as_view(), name='issue-delete'),
    url(r'^issue/(?P<slug>[\w\-]+)/reprocess$',
        reprocess, name='reprocess'),
    url(r'^server-settings', ServerSettingsView.as_view(), name='server-settings'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
