from rest_framework import routers

from . import views


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('', views.UserView, basename='list')
urlpatterns = router.urls
app_name = 'ses'
