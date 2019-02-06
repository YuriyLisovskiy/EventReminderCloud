from django.urls import include
from django.conf.urls import url


urlpatterns = [
	url(r'^accounts/?', include('account.urls')),
	url(r'^auth/', include('rest_auth.urls')),
	url(r'^backups/?', include('backup.urls'))
]
