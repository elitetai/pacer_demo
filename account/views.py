import logging

from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.contenttypes.models import ContentType

from rest_framework import generics, mixins, serializers, status, views, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from account.models import User
from account.serializers import GetScoreSerializer

logger = logging.getLogger('pacer_demo')

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
            logger.warning(f"User ID#[{self.request.data.get('user_id')}] is unrecognised or not provided.")
            raise serializers.ValidationError("User ID is unrecognised or not provided.")

        if not self.request.data.get('score') and not self.request.data.get('score') == 0:
            raise serializers.ValidationError("Score is missing!")
        return qs

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        LogEntry.objects.log_action(
            # user_id = request.user.id,
            user_id = instance.id,
            content_type_id = ContentType.objects.get_for_model(User).pk,
            object_id = instance.id,
            object_repr = str(instance.email),
            action_flag = CHANGE,
            change_message = "Updated an User's detail",
        )

        logger.info(f"User ID#[{instance.id}]: Updated a User's Profile info ")
        return Response(f"User ID #[{instance.id}]: score {instance.score} has been updated!", status=status.HTTP_200_OK)        