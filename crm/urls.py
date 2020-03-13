from django.urls import path, include
from rest_framework import routers

from . import views
from users import views as user_view


router = routers.DefaultRouter()
router.register('users', user_view.MyUserViewSet)
router.register('staff', views.StaffViewSet)
router.register('service-categories', views.ServiceCategoryViewSet)
router.register('services', views.ServiceViewSet)
router.register('days', views.DayViewSet)
router.register('appointments', views.AppointmentViewSet)
router.register('cheques', views.ChequeViewSet)
router.register('stocks', views.StockViewSet)
router.register('expenses', views.ExpenseViewSet)
router.register('status', views.StageViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    # path('send/', user_view.email_to_clients),
]