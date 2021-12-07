from rest_framework import serializers 
from .models import StringCalculator

class StringCalculatorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta: 
        model = StringCalculator
        fields = ('id', 'strReq', 'strRes', 'dtCreated')
        read_only_fields = ('dtCreated',)
        