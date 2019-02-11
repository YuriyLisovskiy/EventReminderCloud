from django.conf.urls import url

from backup.views import BackupListView, BackupDetailsView, BackupCreateView


urlpatterns = [
	url(r'^$', BackupListView.as_view()),
	url(r'^create/?$', BackupCreateView.as_view()),
	url(r'^details/(?P<pk_hash>\w{128})/?$', BackupDetailsView.as_view())
]
