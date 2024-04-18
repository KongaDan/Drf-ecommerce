from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategoySerializer, ProductSerializer

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