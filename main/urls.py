from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SessionViewSet, HelloApiView, get_games, submit_results, display_top_users, display_top_players \
    , display_weekly_report

router = DefaultRouter()
router.register('session', SessionViewSet, basename='session')
urlpatterns = router.urls

urlpatterns += [
    path("hello", HelloApiView.as_view()),
    path('games', get_games, name="games"),
    path('submit/', submit_results, name='submit'),
    path('topresults', display_top_users, name='top-users'),
    path('topplayers', display_top_players, name='top-players'),
    path('weekly_report', display_weekly_report, name='weekly_report'),
]