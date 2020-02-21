import zipfile
from zipfile import BadZipFile
import logging
import os
from io import BytesIO

from PIL import Image


from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
#from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.encoding import force_text
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
#from django.forms.widgets import HiddenInput
from .models import  Photo

logger = logging.getLogger('photologue.forms')

# 供 admin.py 中使用
class UploadZipForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ['zip_file', 'title']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
        
    
    def clean_zip_file(self):
        """Open the zip file a first time, to check that it is a valid zip archive.
        We'll open it again in a moment, so we have some duplication, but let's focus
        on keeping the code easier to read!
        """
        zip_file = self.cleaned_data['zip_file']
        try:
            zip = zipfile.ZipFile(zip_file)
        except BadZipFile as e:
            raise forms.ValidationError(str(e))
        bad_file = zip.testzip()
        if bad_file:
            zip.close()
            raise forms.ValidationError('"%s" in the .zip archive is corrupt.' % bad_file)
        zip.close()  # Close file in all cases.
        return zip_file

    def clean_title(self):
        #title = self.cleaned_data.get('title', None)
        title = self.cleaned_data.get('zip_file', None)
        title = title.name 
        if title and Photo.objects.filter(title=title).exists():
            raise forms.ValidationError(_('A photo with that title already exists.'))
        return title

    def clean(self):
        cleaned_data = super().clean()
        if not self['title'].errors:
            # If there's already an error in the title, no need to add another error related to the same field.
            # 如果标题中已经有错误，则无需添加与同一字段相关的其他错误。
            if not cleaned_data.get('title', None) :
                raise forms.ValidationError(
                    _('Select an existing gallery, or enter a title for a new photo.'))
        return cleaned_data

    def save(self, request=None, zip_file=None):
        if not zip_file:
            zip_file = self.cleaned_data['zip_file']
        zip = zipfile.ZipFile(zip_file)
        count = 1
        
        
        title = self.clean_title()
        
        for filename in sorted(zip.namelist()):

            logger.debug('Reading file "{}".'.format(filename))

            if filename.startswith('__') or filename.startswith('.'):
                logger.debug('Ignoring file "{}".'.format(filename))
                continue

            if os.path.dirname(filename):
                logger.warning('Ignoring file "{}" as it is in a subfolder; all images should be in the top '
                               'folder of the zip.'.format(filename))
                if request:
                    messages.warning(request,
                                     _('Ignoring file "{filename}" as it is in a subfolder; all images should '
                                       'be in the top folder of the zip.').format(filename=filename),
                                     fail_silently=True)
                continue

            data = zip.read(filename)

            if not len(data):
                logger.debug('File "{}" is empty.'.format(filename))
                continue

            
            
            # A photo might already exist with the same slug. 一张照片可能已经存在与相同的弹头。
            # So it's somewhat inefficient, 所以效率有点低，
            # but we loop until we find a slug that's available. 但我们会一直循环直到找到一个可用的弹头
            while True:
                photo_title = ' '.join([title, str(count)])
                slug = slugify(photo_title) # 全部转化成小写字母,空格部分替换成短横线 -  print(slugify('The song of ice and fire ')) # the-song-of-ice-and-fire
                if Photo.objects.filter(slug=slug).exists(): # 判断数据库的记录是否存在
                    count += 1
                    continue
                break

            photo = Photo(title=title,
                          slug=slug)

            # Basic check that we have a valid image. 基本检查我们有一个有效的图像。
            try:
                file = BytesIO(data)
                opened = Image.open(file)
                opened.verify()
            except Exception:
                # Pillow doesn't recognize it as an image.
                # If a "bad" file is found we just skip it.
                # But we do flag this both in the logs and to the user.
                logger.error('Could not process file "{}" in the .zip archive.'.format(
                    filename))
                if request:
                    messages.warning(request,
                                     _('Could not process file "{0}" in the .zip archive.').format(
                                         filename),
                                     fail_silently=True)
                continue

            contentfile = ContentFile(data)
            photo.image.save(filename, contentfile)
            photo.save()
            
            count += 1

        zip.close()


