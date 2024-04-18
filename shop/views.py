from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from .models import Category, Product
from .serializers import *

class CategoryAPIView(APIView):

    def get(self, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategoySerializer(categories, many=True)
        return Response(serializer.data)

    """
    le parametre many permet de preciser au serializer qu'il va devoir generer une liste d'elt a partir de l'iterable

    Seul GET est accessible sur notre endpoint, car nous n’avons redéfini que la méthode  get  dans la View. Ne pas réécrire de méthodes permet de ne pas les rendre accessibles. 
    Nous pourrions réécrire également les méthodes  post,  patch  et  delete.
    """

class ProductAPIview(APIView):

    def get(self, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)
    
class CategoryViewset(ReadOnlyModelViewSet):
    serializer_class=CategoySerializer
   # queryset= Category.objects.all()

    def get_queryset(self):
       return Category.objects.filter(active = True)
    
class ProductViewset(ReadOnlyModelViewSet):
    serializer_class= ProductSerializer
    #queryset= Product.objects.filter(active=True)

    def get_queryset(self):
        queryset= Product.objects.filter(active=True)
        category_id=self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id= category_id)
        return queryset
    
class ArticleViewset(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    def get_queryset(self):
        queryset= Article.objects.filter(active= True)
        product_id=self.request.GET.get('product_id')
        if product_id is not None:
            queryset=queryset.filter(product_id=product_id)
        return queryset
    
    
   