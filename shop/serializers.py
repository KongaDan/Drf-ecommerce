from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from shop.models import Category, Product, Article

class ArticleSerializer(ModelSerializer):

    class Meta:
        model= Article
        fields =['id','date_created','date_updated','name','price','product_id']

    def validate_price(self, value):
        if not value > 1 :
            raise serializers.ValidationError(' Price must be > 1')
        return value

    def validate(self, data):
        product_id = data['product_id']
        product = Product.objects.get(product_id)
        if product.active is False:
            raise serializers.ValidationError(' le produit associe doit etre actif')
        return data 

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

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists() :
            #DRF met a disposition l'exception ValidationError
            raise serializers.ValidationError('Category already exists')
        return value
    
    def validate(self, data):
        if data['name'] not in data['description']:
            raise serializers.ValidationError('Name must be in description')
        return data

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

