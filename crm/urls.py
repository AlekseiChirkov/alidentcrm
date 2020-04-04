from django.urls import path, include
from rest_framework import routers

from . import views
from users import views as user_view


router = routers.DefaultRouter()
router.register('users', user_view.MyUserViewSet)
router.register('staff', views.StaffViewSet)
router.register('clients', views.ClientViewSet)
router.register('service-categories', views.ServiceCategoryViewSet)
router.register('services', views.ServiceViewSet)
router.register('stocks', views.StockViewSet)
router.register('days', views.DayViewSet)
router.register('appointments', views.AppointmentViewSet)
router.register('expenses', views.ExpenseViewSet)
router.register('reports', views.ReportViewSet)
router.register('incomes', views.IncomeViewSet)


urlpatterns = [
    path('crm/', include(router.urls)),
    path('', views.home, name='home'),
    # path('send/', user_view.email_to_clients),
]