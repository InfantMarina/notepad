from rest_framework import serializers
from notepad import models

class Storage_Serializers(serializers.ModelSerializer):
    
    class Meta:
        model = models.Storage
        fields = "__all__"
        