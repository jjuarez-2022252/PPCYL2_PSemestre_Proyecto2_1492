from django.urls import path
from .views import login_view, logout_view, admin_dashboard, tutor_dashboard, ver_notas
from .views import login_view, logout_view, admin_dashboard, tutor_dashboard, ver_notas, reporte_pdf_tutor

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('tutor-dashboard/', tutor_dashboard, name='tutor_dashboard'),
    path('notas/', ver_notas, name='ver_notas'),
path('tutor-reporte-pdf/', reporte_pdf_tutor, name='reporte_pdf_tutor'),
]