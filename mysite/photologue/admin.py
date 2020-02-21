from django import forms
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import helpers
#from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ungettext, ugettext_lazy as _

from .forms import UploadZipForm
from .models import Photo

MULTISITE = getattr(settings, 'PHOTOLOGUE_MULTISITE', False)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'image',)
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(r'^upload_zip/$',
                self.admin_site.admin_view(self.upload_zip),
                name='photologue_upload_zip')
        ]
        #print('custom_urls, urls ==== ', custom_urls,'---------', urls)
        return custom_urls + urls

    def upload_zip(self, request):

        context = {
            'title': _('Upload a zip archive of photos'),
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }

        # Handle form request
        if request.method == 'POST':
            form = UploadZipForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(request=request)
                return HttpResponseRedirect('..')
        else:
            form = UploadZipForm()
        context['form'] = form
        context['adminform'] = helpers.AdminForm(form,
                                                 list([(None, {'fields': form.base_fields})]), 
                                                 {})
        return render(request, 'admin/photologue/photo/upload_zip.html', context)



admin.site.register(Photo, PhotoAdmin)



