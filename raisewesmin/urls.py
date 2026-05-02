from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from raisewesmin.views import signup_view
from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),

    # Auth URLs
    path("login/", auth_views.LoginView.as_view(template_name='registration/login.html'), name="login"),
    # Adding next_page ensures that after the POST logout, it knows where to go
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", signup_view, name="signup"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.auth import views as auth_views
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Wagtail URLs should always be last
urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]