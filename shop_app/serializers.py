from rest_framework import serializers
from .models import Book, Product, User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','role']
        
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        #fields = '__all__'
        fields = ['id','title','author','published_date','price']
        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        #fields = '__all__'
        fields = ['id','name','description','price','stock','sku']
        
class LogoutResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
      
