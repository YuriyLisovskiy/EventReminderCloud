from rest_framework import (
	status,
	permissions,
	authentication
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView

from backup.models import Backup
from backup.serializers import BackupSerializer


class BackupListView(ListCreateAPIView):
	queryset = Backup.objects.all().order_by('-timestamp')
	serializer_class = BackupSerializer
	authentication_classes = (authentication.TokenAuthentication,)
	# permission_classes = (permissions.IsAuthenticated,)
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class BackupDetailsView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	# permission_classes = (permissions.IsAuthenticated,)
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	@staticmethod
	def get(request, pk):
		if pk is None:
			return Response({'details': 'id is not provided'}, status=status.HTTP_400_BAD_REQUEST)
		backup = Backup.get_by_id(pk)
		if backup is None:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializer = BackupSerializer(backup)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@staticmethod
	def post(request, pk):
		if pk is None:
			return Response({'details': 'id is not provided'}, status=status.HTTP_400_BAD_REQUEST)
		backup = Backup.remove(pk)
		if backup is None:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializer = BackupSerializer(backup)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
