from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from auth_token_app.models import User, Story
from auth_token_app.serializers import UserSerializer, StorySerializer

class MeMixin:

    @action(methods=['get', 'patch'], detail=False)
    def me(self, request):
        serializer = self.get_serializer_class()

        if request.method == 'GET' and 'GET' in self.get_me_config().get('allowed_methods'):

            data = serializer(
                instance=self.get_me_config().get('instance'),
                many=self.get_me_config().get('many')
            ).data
            return Response(data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH' and 'PATCH' in self.get_me_config().get('allowed_methods'):
            user = User.objects.get(user_id=request.user.user_id)
            data = serializer(user, request.data, partial=True)
            data.is_valid(raise_exception=True)
            data.save()
            return Response({
                'message': "User Profile Updated"
            },
                status=status.HTTP_200_OK,
            )

        else:
            return Response({
                'message': f"Unsupported method {request.method}.",
            },
                status=status.HTTP_400_BAD_REQUEST
            )


class UserViewSet(MeMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    viewset_serializers = {
        'me': {
            'get': UserSerializer,
            'patch': UserSerializer
        },

    }

    def get_serializer_class(self):
        return self.viewset_serializers.get(self.action).get(self.request.method)

    def get_queryset(self):
        return User.objects.all()

    def get_me_config(self):
        return {
            'instance': self.request.user,
            'many': False,
            'allowed_methods': ['get', 'patch']
        }


class StoryViewSet(MeMixin, GenericViewSet):
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Story.objects.all()

    def get_me_config(self):
        return {
            'instance': self.request.user,
            'many': False,
            'allowed_methods': ['get']
        }


