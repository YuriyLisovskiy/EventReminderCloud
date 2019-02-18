from django.urls import include
from django.conf.urls import url

from rest_auth.views import LogoutView

from account.views import LoginAPIView


urlpatterns = [
	url(r'^login/?', LoginAPIView.as_view()),
	url(r'^logout/?', LogoutView.as_view()),
	url(r'^accounts/', include('account.urls')),
	url(r'^backups/', include('backup.urls'))
]
