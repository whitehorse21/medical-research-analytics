from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LiteratureArticleViewSet, ParticipantViewSet, StudyViewSet
from .auth_views import login_view, logout_view, signup, user_info

router = DefaultRouter()
router.register("studies", StudyViewSet, basename="study")
router.register("participants", ParticipantViewSet, basename="participant")
router.register("literature", LiteratureArticleViewSet, basename="literature")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/signup/", signup, name="signup"),
    path("auth/login/", login_view, name="login"),
    path("auth/logout/", logout_view, name="logout"),
    path("auth/user/", user_info, name="user-info"),
]
