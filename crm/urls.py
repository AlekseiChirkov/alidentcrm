from django.urls import path, include
from rest_framework import routers

from . import views
from users import views as user_view


router = routers.DefaultRouter()
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
router.register('cheques', views.ChequeViewSet)
router.register('user-appointments', views.UserAppointmentsViewSet)
router.register('doctor-appointments', views.DoctorAppointmentsViewSet)


urlpatterns = [
    path('', views.home, name='home'),
    path('crm/', include(router.urls)),
    path('crm/users/', user_view.RegistrationAPIView.as_view()),
    path('crm/login/', user_view.LoginAPIView.as_view()),
]
