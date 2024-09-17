from rest_framework import  serializers
from App_db.models.file_handover_mt import FileHandOver
from IntelliSync_db.models import LocationMaster


class FileHandOverSerializer(serializers.ModelSerializer):
    
    class  Meta:
       model =FileHandOver
       fields = '__all__'
       
    def create(self, validated_data):
        return FileHandOver.objects.using('is_app').create(**validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save(using='is_app')  # Save using 'is_app' database
        return instance
    
