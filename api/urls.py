from django.urls import include, path 
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'stringCalc', views.StringCalcViewSet)

urlpatterns = [
    path('', include(router.urls)),
]