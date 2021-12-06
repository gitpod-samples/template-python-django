from rest_framework import views 
from rest_framework import status
from rest_framework.response import Response 

# Create your views here.

class stringCalc(views.APIView):

    def post(self, request): 
        str strParam = request.DATA.get('str_numbers')
        p1 , p2 = strParam.split()
        result = (int) p1 + (int)p2 
        return Response(result)