from rest_framework.routers import SimpleRouter

from movies.views import PublicMovieViewSet

router = SimpleRouter()
router.register('movies', PublicMovieViewSet, basename='movies')

urlpatterns = router.urls
