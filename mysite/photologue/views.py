from django.views.generic.dates import ArchiveIndexView, DateDetailView, DayArchiveView, MonthArchiveView, \
    YearArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Photo


# Photo views.

class PhotoListView(ListView):
    queryset = Photo.objects.all()
    paginate_by = 20


class PhotoDetailView(DetailView):
    pass
    #queryset = Photo.objects.on_site().is_public()


class PhotoDateView:
    #queryset = Photo.objects.on_site().is_public()
    #date_field = 'date_added'
    allow_empty = True


class PhotoDateDetailView(PhotoDateView, DateDetailView):
    pass


class PhotoArchiveIndexView(PhotoDateView, ArchiveIndexView):
    pass


class PhotoDayArchiveView(PhotoDateView, DayArchiveView):
    pass


class PhotoMonthArchiveView(PhotoDateView, MonthArchiveView):
    pass


class PhotoYearArchiveView(PhotoDateView, YearArchiveView):
    make_object_list = True
