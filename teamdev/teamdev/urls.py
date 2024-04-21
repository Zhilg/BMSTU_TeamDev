from django.urls import path, include

from .views import views
from drf_spectacular.views import SpectacularAPIView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="LMS",
        default_version="v1",
        description="BMSTU_WEB COURSE",
        
    ),
    public=True
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("auth/register", views.UserRegisterView.as_view(), name='register'),
    path("auth/login", views.UserLoginView.as_view(), name="login"),
    path('auth/logout', views.LogoutView.as_view(), name='logout_view'),
    
    path("userprofiles", views.UserProfilesView.as_view(), name='list_users'),
    path("userprofiles/<int:id>", views.SingleUserView.as_view()),
    path("tasks", views.TasksView.as_view()),
    path("tasks/<int:id>", views.SingleTaskView.as_view()),
    path("taskpacks", views.TaskPacksView.as_view()),
    path("taskpacks/<int:id>", views.SingleTaskPackView.as_view()),
    path("solutions", views.SolutionsView.as_view()),
    path("solutions/<int:id>", views.SingleSolutionView.as_view()),
    
]
