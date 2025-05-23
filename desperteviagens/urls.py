from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from viagens.custom_admin import custom_admin_site
from django.contrib.sitemaps.views import sitemap
from viagens.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),

    # 👇 Rotas customizadas do painel devem vir ANTES
    path('painel/dashboard/', include(('viagens.urls_painel', 'viagens_painel'), namespace='painel')),
  # ROTAS PERSONALIZADAS

    path('painel/', custom_admin_site.urls),  # ROTAS DO DJANGO ADMIN CUSTOM
    
    path('', include('viagens.urls')),  # SITE
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
