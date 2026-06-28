from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from courses.views import DepartmentViewSet, CourseViewSet, StudentViewSet, EnrollmentViewSet

router = routers.DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'students', StudentViewSet)
router.register(r'enrollments', EnrollmentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
