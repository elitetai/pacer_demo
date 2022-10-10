from rest_framework import serializers

from account.models import User


class GetScoreSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(required=True, queryset=User.objects.all())
    score = serializers.IntegerField(min_value=0)
    
    class Meta:
        model = User
        fields = ['user_id', 'score']

    def validate_score(self, value):
        return (value + 100)//2