from rest_framework import  serializers
from App_db.models.file_handover_mt import FileHandOver


class FileHandOverSerializer(serializers.ModelSerializer):
    class  Meta:
       model =FileHandOver
       fields = '__all__'
       
       
       
       
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    