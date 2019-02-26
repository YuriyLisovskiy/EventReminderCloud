import jwt
import random
import threading
from hashlib import sha256

from rest_framework import (
	permissions,
	authentication
)
from django.template.loader import render_to_string

from account.models import Account
from account.util import gen_password, token_is_valid, send_email
from account.serializers import AccountSerializer, AccountDetailsSerializer

from django.conf import settings

from rest_framework import status
from rest_auth.views import LoginView
from rest_framework.views import APIView
from rest_framework.response import Response


class AccountCreateAPIView(APIView):

	def post(self, request):
		password = gen_password()
		data = request.data.copy()
		data['password'] = password
		serializer = AccountSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			threading.Thread(target=self._send_credentials, kwargs=data).start()
			return Response({'detail': 'account has been created'}, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@staticmethod
	def _send_credentials(email, username, password):
		html = render_to_string('credentials_email.html', {
			'username': ''.join(username),
			'password': ''.join(password)
		})
		plain = open(
			'{}/templates/credentials_email.txt'.format(settings.BASE_DIR)
		).read().replace('{{ username }}', ''.join(username)).replace('{{ password }}', ''.join(password))
		send_email('Registration of Event Reminder account', html, plain, [email], settings.EMAIL_HOST_USER)


class AccountDeleteAPIView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	@staticmethod
	def post(request):
		Account.remove(request.user.username)
		return Response({'detail': 'account hash been deleted'}, status=status.HTTP_201_CREATED)


class SendTokenAPIView(APIView):

	def post(self, request):
		email = request.data.get('email')
		if email is None:
			return Response({'detail': 'email was not provided'}, status=status.HTTP_400_BAD_REQUEST)
		account = Account.objects.filter(email=email).first()
		if account is None:
			return Response({'detail': 'account is not found'}, status=status.HTTP_404_NOT_FOUND)
		nonce = sha256(
			''.join([account.password, str(random.randrange(-999999, 999999))]).encode()
		).hexdigest()
		payload = {
			'email': account.email,
			'username': account.username,
			'password': account.password,
			'nonce': nonce
		}
		jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

		threading.Thread(target=self._send_confirmation, args=(
			account.email, account.username, sha256(jwt_token).hexdigest()
		)).start()

		request.session['{}_nonce'.format(account.email)] = nonce
		return Response({'detail': 'confirmation email has been sent'}, status=status.HTTP_201_CREATED)

	@staticmethod
	def _send_confirmation(email, username, jwt_token, sender=settings.EMAIL_HOST_USER):
		html = render_to_string('reset_password_email.html', {
			'token': jwt_token,
			'username': username
		})
		plain = open(
			'{}/templates/reset_password_email.txt'.format(settings.BASE_DIR)
		).read().replace('{{ token }}', jwt_token).replace('{{ username }}', username)
		send_email('Reset your Event Reminder password', html, plain, [email], sender)


class ResetPasswordAPIView(APIView):

	@staticmethod
	def post(request):
		email = request.data.get('email')
		if email is None:
			return Response({'detail': 'email was not provided'}, status=status.HTTP_400_BAD_REQUEST)
		account = Account.objects.filter(email=email).first()
		if account is None:
			return Response({'detail': 'account is not found'}, status=status.HTTP_404_NOT_FOUND)
		if 'confirmation_token' not in request.data:
			return Response({'detail': 'missing confirmation token'}, status=status.HTTP_400_BAD_REQUEST)
		nonce = request.session.get('{}_nonce'.format(account.email), '')
		if token_is_valid(account, settings.SECRET_KEY, nonce, request.data.get('confirmation_token', '')):
			new_password = request.data.get('new_password', None)
			new_password_confirm = request.data.get('new_password_confirm', None)
			if new_password is None or new_password_confirm is None:
				return Response({'detail': 'missing new password or its confirmation'}, status=status.HTTP_400_BAD_REQUEST)
			if new_password != new_password_confirm:
				return Response({'detail': 'password confirmation failed'}, status=status.HTTP_400_BAD_REQUEST)
			data = request.data.copy()
			data['username'] = account.username
			data['password'] = new_password
			serializer = AccountSerializer(instance=account, data=data)
			if serializer.is_valid():
				serializer.save()
				del request.session['{}_nonce'.format(account.email)]
				return Response({'detail': 'password has been changed'}, status=status.HTTP_201_CREATED)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'detail': 'confirmation token is incorrect'}, status=status.HTTP_400_BAD_REQUEST)


class AccountDetailsAPIView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	@staticmethod
	def get(request):
		account = Account.get_by_pk(request.user.username)
		if account is None:
			return Response({'detail': 'account is not found'}, status=status.HTTP_404_NOT_FOUND)
		serializer = AccountDetailsSerializer(account)
		return Response(serializer.data, status=status.HTTP_200_OK)


class AccountEditAPIView(APIView):
	authentication_classes = (authentication.TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	@staticmethod
	def post(request):
		account = Account.get_by_pk(request.user.username)
		if account is None:
			return Response({'detail': 'account is not found'}, status=status.HTTP_404_NOT_FOUND)
		serializer = AccountSerializer(instance=account, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'detail': 'account has been edited'}, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(LoginView):

	def post(self, request, *args, **kwargs):
		self.request = request
		self.serializer = self.get_serializer(data=self.request.data, context={'request': request})
		self.serializer.is_valid(raise_exception=True)

		self.login()

		if self.user.is_activated is False:
			self.user.edit(is_activated=True).save()

		return self.get_response()
