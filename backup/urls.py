from django.conf.urls import url

from backup.views import BackupListView, BackupDetailsView


urlpatterns = [
	url(r'^$', BackupListView.as_view()),
	url(r'^get/?$', BackupDetailsView.as_view())
]
