from rest_framework.serializers import ModelSerializer

from shop.models import Category, Product, Article

class CategoySerializer(ModelSerializer):
    class Meta:
        model=Category
        fields = ['id','name']

class ProductSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields = ['id','date_created','date_updated','name','category_id']

class ArticleSerializer(ModelSerializer):
    class Meta:
        model= Article
        fields =['id','date_created','date_updated','name','price','product_id']