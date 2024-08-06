from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Food, FoodCategory, FoodListSerializer


class GetFoodsInfoView(APIView):

    def get(self, request):
        queryset = FoodCategory.objects.filter(food__is_publish=True).distinct().values()

        for cat in queryset:
            foods = Food.objects.filter(is_publish=True, category__name_ru=cat["name_ru"]).distinct()
            changed_foods = foods.values()
            for food, change in zip(foods, changed_foods):
                additional = food.additional.filter(is_publish=True).distinct()
                change["additional"] = additional
            cat["food"] = changed_foods
        serializer_for_queryset = FoodListSerializer(
            instance=queryset,
            many=True,

        )
        return Response(serializer_for_queryset.data)
