from django.conf.urls import url
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from .views import PhotoListView, PhotoDetailView, \
    PhotoArchiveIndexView, PhotoDateDetailView, PhotoDayArchiveView, \
    PhotoYearArchiveView, PhotoMonthArchiveView


app_name = 'photologue'
urlpatterns = [

    url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
        PhotoDateDetailView.as_view(month_format='%m'),
        name='photo-detail'),
    url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
        PhotoDayArchiveView.as_view(month_format='%m'),
        name='photo-archive-day'),
    url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
        PhotoMonthArchiveView.as_view(month_format='%m'),
        name='photo-archive-month'),
    url(r'^photo/(?P<year>\d{4})/$',
        PhotoYearArchiveView.as_view(),
        name='pl-photo-archive-year'),
    url(r'^photo/$',
        PhotoArchiveIndexView.as_view(),
        name='pl-photo-archive'),
 
    url(r'^photo/(?P<slug>[\-\d\w]+)/$',
        PhotoDetailView.as_view(),
        name='pl-photo'),
    url(r'^photolist/$',
        PhotoListView.as_view(),
        name='photo-list'),
]
