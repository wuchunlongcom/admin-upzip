from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.static import serve

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    
    url(r'^photologue/', include('photologue.urls')),
    url(r'^$', TemplateView.as_view(template_name="homepage.html"), name='homepage'),
    
    # 处理 media 信息，用于图片获取
    url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    
    #url(r'^$', RedirectView.as_view(url='/account/index/', query_string=True)),
    #url(r'^$', RedirectView.as_view(url='/login/', query_string=True)),

] #+ static(settings.STATIC_URL, document_root=settings.STATIC_URL)
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)