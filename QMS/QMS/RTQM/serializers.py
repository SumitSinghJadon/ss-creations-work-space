from rest_framework import  serializers
from QMS_db.models import OrderMt, OrderDt ,ObDetail

class OrderMtSerializer(serializers.ModelSerializer):
    class  Meta:
       model =OrderMt
       fields = '__all__'
       
       
class OrderDtSerializer(serializers.ModelSerializer):
    order_mt = OrderMtSerializer() 
    class Meta:
        model =OrderDt
        fields  = '__all__'
        
        
class ObDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model =ObDetail
        fields = '_all_'