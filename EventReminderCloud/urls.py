from django.urls import include
from django.conf.urls import url


urlpatterns = [
	url(r'^api/v1/', include('api.urls')),
]
