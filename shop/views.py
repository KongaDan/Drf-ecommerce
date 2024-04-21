from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from .models import Category, Product
from .serializers import *
from rest_framework.decorators import action
from django.db import transaction

class MultipleSerializerMixin:
    #Un Mixin est une classe qui ne fonctionne pas de facon autonome
    # Elle permet d'ajouter des fonctionnalites aux classes qui les etendent

    detail_serializer_class = None

    def get_serializer_class(self):
        # NOtre mixin determine quel serializer a utiliser
        # meme si elle ne sait pas ce que c'est 

        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            # si l'action demandee est le detail alors nous retournons le serialiser de detail
            return self.detail_serializer_class
        return super().get_serializer_class() 

class CategoryAPIView(APIView):

    def get(self, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)

    """
    le parametre many permet de preciser au serializer qu'il va devoir generer une liste d'elt a partir de l'iterable

    Seul GET est accessible sur notre endpoint, car nous n’avons redéfini que la méthode  get  dans la View. Ne pas réécrire de méthodes permet de ne pas les rendre accessibles. 
    Nous pourrions réécrire également les méthodes  post,  patch  et  delete.
    """

class ProductAPIview(APIView):

    def get(self, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductListSerializer(products,many=True)
        return Response(serializer.data)
    
class CategoryViewset(MultipleSerializerMixin ,ReadOnlyModelViewSet):
    serializer_class=CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
       return Category.objects.filter(active = True)
    
    @action(detail = True ,methods = ['post'])
    def disable(self, request, pk ):
        # Nous avons défini notre action accessible sur la méthode POST seulement
        # elle concerne le détail car permet de désactiver une catégorie

        # Nous avons également mis en place une transaction atomique car plusieurs requêtes vont être exécutées
        # en cas d'erreur, nous retrouverions alors l'état précédent

        # Désactivons la catégorie
        self.get_object().disable()

        return Response()

class ProductViewset(MultipleSerializerMixin ,ReadOnlyModelViewSet):
    serializer_class= ProductListSerializer
    #queryset= Product.objects.filter(active=True)
    detail_serializer_class = ProductDetailSerializer

    def get_queryset(self):
        queryset= Product.objects.filter(active=True)
        category_id=self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id= category_id)
        return queryset
    @action(detail = True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()
    
class ArticleViewset(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    def get_queryset(self):
        queryset= Article.objects.filter(active= True)
        product_id=self.request.GET.get('product_id')
        if product_id is not None:
            queryset=queryset.filter(product_id=product_id)
        return queryset
    
    
   