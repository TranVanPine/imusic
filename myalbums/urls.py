
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('', index, name='index'),
	path('category/', CategoryListView.as_view(), name='category'),
	path('category/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
	path('song/', SongListView.as_view(), name='song'),
	path('artist/', ArtistListView.as_view(), name='artist'),
	path('artist/<int:pk>', ArtistDetailView.as_view(), name='artist-detail'),
	path('songs/', include([
		path('<int:pk>', SongDetailView.as_view(), name='song-detail'),
		path('upload', SongUploadView.as_view(), name='upload'),
		path('<slug:id>', SongUploadDetailsView.as_view(), name='upload-details'),
		])),
	path('register/', register, name='register'),
    path('profile',profile, name ='profile'),
    path('hotsong/', HotSongListView.as_view(), name='hot-song'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

