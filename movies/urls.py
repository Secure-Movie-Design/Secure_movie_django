from rest_framework.routers import SimpleRouter

from movies.views import PublicMovieViewSet, LikesViewSet

router = SimpleRouter()
router.register('movies', PublicMovieViewSet, basename='movies')
router.register('likes', LikesViewSet, basename='likes')

urlpatterns = router.urls
