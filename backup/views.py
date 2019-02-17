from rest_framework import (
	status,
	permissions,
	authentication
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView

from backup.models import Backup
from backup.serializers import BackupSerializer, BackupListSerializer


class BackupListView(ListAPIView):
	serializer_class = BackupListSerializer
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def get_queryset(self):
		return Backup.objects.filter(account=self.request.user).order_by('-timestamp')


class BackupCreateView(CreateAPIView):
	serializer_class = BackupSerializer
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)


class BackupDetailsView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	@staticmethod
	def get(request, pk_hash):
		if pk_hash is None:
			return Response({'details': 'primary key is not provided'}, status=status.HTTP_400_BAD_REQUEST)
		backup = Backup.get_by_pk(pk_hash)
		if backup is None:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializer = BackupSerializer(backup)
		return Response(serializer.data, status=status.HTTP_200_OK)


class BackupDeleteView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	@staticmethod
	def post(request, pk_hash):
		if pk_hash is None:
			return Response({'details': 'primary key is not provided'}, status=status.HTTP_400_BAD_REQUEST)
		backup = Backup.remove(pk_hash)
		if backup is None:
			return Response(status=status.HTTP_404_NOT_FOUND)
		return Response({'detail': 'backup {} has been deleted'.format(backup.digest)}, status=status.HTTP_201_CREATED)
