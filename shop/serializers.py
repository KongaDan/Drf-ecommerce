from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from shop.models import Category, Product, Article

class ArticleSerializer(ModelSerializer):

    class Meta:
        model= Article
        fields =['id','date_created','date_updated','name','price','product_id']

"""
Pour cela, nous pouvons redéfinir notre attribut de classe products 
avec un SerializerMethodField  qui nous donne alors la possibilité de filtrer les produits à retourner.
"""
class ProductDetailSerializer(ModelSerializer):

    articles = serializers.SerializerMethodField()

    class Meta:
        model=Product
        fields = ['id','date_created','date_updated','name','category_id','articles']

    def get_articles(self, instance):
        queryset = instance.articles.filter(active = True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data
    
class ProductListSerializer(ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['id','date_created','date_updated','name']
        
class CategoryListSerializer(ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id','date_created','date_updated','name']

class CategoryDetailSerializer(ModelSerializer):
    
    #products = ProductSerializer(many= True)
    products= serializers.SerializerMethodField()

    class Meta:
        model=Category
        fields = ['id','date_created','date_updated','name', 'products']

    #Pour retourner que le produits actifs
    def get_products(self, instance):
        queryset= instance.products.filter(active = True)

        serializer= ProductDetailSerializer(queryset, many=True)
        return serializer.data

