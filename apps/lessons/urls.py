from django.urls import path

from . import views as lessons_views


app_name = "apps_lessons"

urlpatterns = [
    path("t-7.4/", lessons_views.T74View.as_view(), name="t74"),
    path("t-7.4/<uuid>/", lessons_views.T74View.as_view(), name="t74_uuid"),
]
