from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
#from rest_framework import viewsets 

from .serializers import StringCalculatorSerializer
from .models import StringCalculator 

# Create your views here.

# class StringCalcViewSet(viewsets.ModelViewSet):
#     queryset = StringCalculator.objects.all()
#     serializer_class = StringCalculatorSerializer

class StringCalcView(APIView):
    def get(self, request, format = None):
        calcs = StringCalculator.objects.all()
        serializer = StringCalculatorSerializer(calcs, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = StringCalculatorSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(strRes = self.add(serializer.validated_data['strReq']))
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def add(self, strParam): 
        p1 , p2 = strParam.split(",")
        result = int(p1) + int(p2) 
        return result

    