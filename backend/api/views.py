from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from rest_framework import generics, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """Создание и получение пользователей"""
    permission_classes = (AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post']


class UserDetailsView(generics.ListAPIView):
    """Получение модели пользователя по токену"""
    serializer_class = UserSerializer
    def get_queryset(self):
        token = self.request.headers.get('Authorization').split(' ')[1]
        try:
            decoded_token = AccessToken(token)
        except TokenError:
            raise PermissionDenied('Invalid token')

        queryset = User.objects.filter(pk=int(decoded_token['user_id']))
        return queryset


class UserConfirmEmailView(APIView):
    """Активация аккаунта, выдача токенов авторизации"""
    permission_classes = (AllowAny, )
    def get(self, request, pk, token):
        user = User.objects.get(pk=pk)
        if user.is_active:
            return Response({'message': 'Account has already been activated'})
        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            html_message = render_to_string('registration/welcome_mail.html')
            message = strip_tags(html_message)
            mail = EmailMultiAlternatives(
                'Welcome to INtouch!',
                message,
                'info@intouch.care',
                [user.email],
            )
            mail.attach_alternative(html_message, 'text/html')
            mail.send()
            return Response({
                'message': 'Account activated',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })
        else:
            return Response({'error': 'Account not activated'})


class PasswordResetRequestView(APIView):
    """Запрос на сброс пароля"""
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        url = f'/reset-password/{user.pk}/{token}/'
        current_site = 'http://85.31.237.54'
        html_message = render_to_string(
            'registration/password_reset.html',
            {'url': url, 'domen': current_site, 'name': user.first_name}
        )
        message = strip_tags(html_message)
        mail = EmailMultiAlternatives(
            'Password Reset for INtouch Account',
            message,
            'info@intouch.care',
            [email],
        )
        mail.attach_alternative(html_message, 'text/html')
        mail.send()
        return Response({"message": "Password reset email sent."})


class PasswordResetConfirmView(generics.GenericAPIView):
    """Подтверждение сброса пароля, выдача токенов авторизации"""
    permission_classes = (AllowAny,)
    def get(self, request, pk, token):
        user = User.objects.get(pk=pk)
        if user and default_token_generator.check_token(user, token):
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Password reset successful',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })
        else:
            return Response({'error': 'Password not reset'})


class PasswordResetCompleteView(APIView):
    """Установка нового пароля пользователя"""
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        user = request.user
        if user:
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successfully'})
        else:
            return Response({'error': 'Password not reset'})


class UpdatePasswordView(APIView):
    """Изменение существующего пароля пользователя"""
    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        user = request.user
        if user and check_password(serializer.validated_data['password'], user.password):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'})
        else:
            return Response({'error': 'Password not changed'})


class UpdateUserView(generics.UpdateAPIView):
    """Редактирование пользовательских данных"""
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer


@api_view(['GET'])
def user_delete_hard(request):
    """Полное удаление пользователя"""
    user = request.user
    if user:
        user.delete()
        return Response({'message': 'User deleted successfully'})
    else:
        return Response({'error': 'User not found'})


@api_view(['GET'])
def user_delete_soft(request):
    """Перевод пользователя в неактивные"""
    user = request.user
    if user:
        user.is_active = False
        user.save()
        return Response({'message': 'User deactivated successfully'})
    else:
        return Response({'error': 'User not found'})


class ClientDeleteView(APIView):
    """Удаление аккаунта клиента из интерфейса доктора"""
    def delete(self, request, pk):
        try:
            client = User.objects.get(pk=pk)
            if request.user.doctor.clients.filter(pk=client.pk).exists():
                client.delete()
                return Response({'message': 'Client deleted successfully'})
        except User.DoesNotExist:
            return Response({'error': 'Client not found'})


class AddClientView(APIView):
    """Добавление нового клиента из интерфейса доктора"""
    def post(self, request):
        serializer = AddClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()
        user = request.user
        user.doctor.clients.add(client)
        return Response({"message": "Confirm email sent."})


class UpdateClientView(generics.UpdateAPIView):
    """Завершение регистрации из интерфейса клиента, установка пароля"""
    queryset = User.objects.all()
    serializer_class = UpdateClientSerializer


class DoctorUpdateClientView(generics.UpdateAPIView):
    """Редактирование доктором данных о клиенте"""
    queryset = User.objects.all()
    serializer_class = DoctorUpdateClientSerializer


# class AssignmentLikeView(APIView):
#     def get(self, request, pk):
#         assignment = Assignment.objects.get(pk=pk)
#         assignment.like()
#         assignment.save()
#         return Response({'message': 'Like.'})
#
#
# class AssignmentDislikeView(APIView):
#     def get(self, request, pk):
#         assignment = Assignment.objects.get(pk=pk)
#         assignment.dislike()
#         assignment.save()
#         return Response({'message': 'Dislike.'})


class AssignmentAddUserMyListView(APIView):
    """Добавление задачи в свой список"""
    def get(self, request, pk):
        user = request.user
        assignment = Assignment.objects.get(pk=pk)
        user.doctor.assignments.add(assignment)
        return Response({'message': 'Assignment added successfully.'})


class AssignmentDeleteUserMyListView(APIView):
    """Удаение задачи из своего списка"""
    def get(self, request, pk):
        user = request.user
        assignment = Assignment.objects.get(pk=pk)
        user.doctor.assignments.remove(assignment)
        return Response({'message': 'Assignment deleted successfully.'})


class AddAssignmentClientView(APIView):
    """Назначение задачи клиенту"""
    def get(self, request, pk, client_pk):
        assignment = Assignment.objects.get(pk=pk)
        client = User.objects.get(pk=client_pk)
        assignments_copy = AssignmentClient.objects.create(
            title=assignment.title,
            text=assignment.text,
            author=assignment.author,
            assignment_type=assignment.assignment_type,
            tags=assignment.tags,
            language=assignment.language,
            share=assignment.share,
            likes=assignment.likes,
            image_url=assignment.image_url,
            user=client,
        )
        blocks = assignment.blocks.all()
        for block in blocks:
            block_copy = Block.objects.create(
                question=block.question,
                type=block.type,
                description=block.description,
                reply=block.reply,
                start_range=block.start_range,
                end_range=block.end_range,
            )
            choice_replies = block.choice_replies.all()
            for choice_reply in choice_replies:
                choice_reply_copy = BlockChoice.objects.create(
                    block=block_copy,
                    reply=choice_reply.reply,
                    checked=choice_reply.checked,
                )
                block_copy.choice_replies.add(choice_reply_copy)
            assignments_copy.blocks.add(block_copy)
        client.client.assignments.add(assignments_copy)
        assignment.share += 1
        assignment.save()
        return Response({'message': 'Assignment set client successfully.'})


class AssignmentViewSet(viewsets.ModelViewSet):
    """CRUD операции над задачами доктора"""
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def destroy(self, request, *args, **kwargs):
        assignment = self.get_object()
        if assignment.author != request.user:
            raise PermissionDenied(
                "You don't have permission to delete this assignment.")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        assignment = self.get_object()
        if assignment.author != request.user:
            raise PermissionDenied(
                "You don't have permission to update this assignment.")
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def draft(self, request, pk):
        """Сокрытие задачи из общего пула"""
        assignments = self.get_object()
        assignments.is_public = False
        assignments.save()
        return Response({'message': 'Assignments saved in draft'})


class AssignmentClientViewSet(viewsets.ModelViewSet):
    """CRUD операции над задачами клиента"""
    queryset = AssignmentClient.objects.all()
    serializer_class = AssignmentClientSerializer

    @action(detail=True, methods=['get'])
    def complete(self, request, pk):
        """Смена статуса задачи на 'done'"""
        assignment = self.get_object()
        assignment.status = 'done'
        assignment.save()
        return Response({'message': 'Status is done'})


class NoteViewSet(viewsets.ModelViewSet):
    """CRUD операции над заметками"""
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
