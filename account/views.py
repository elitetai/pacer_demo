from rest_framework import (generics, mixins, serializers, status, views,
                            viewsets)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from account.models import User
from account.serializers import GetScoreSerializer

# get username / email + score

# get_score
class GetScoreView(generics.UpdateAPIView):
    """
    Description - This API is to update and obtain user's score.
    """
    # permission_classes = (IsAuthenticated, )
    permission_classes = (AllowAny, )
    serializer_class   = GetScoreSerializer

    def get_object(self):    
        try:
            qs = User.objects.get(pk=self.request.data.get('user_id'))
        except Exception:
            # logger.warning(
            #     "User ID#[%s] is unrecognised or not provided.", self.request.data.get('user_id'))
            raise serializers.ValidationError('User id is unrecognised or not provided.')
        return qs

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(f'User ID #{instance.id}: score {instance.score} has been updated!', status=status.HTTP_200_OK)        