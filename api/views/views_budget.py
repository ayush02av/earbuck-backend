from api.views.views import *
from api.serializers import serializers_budget

class budget(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers_budget.budget_serializer

    def get(self, request):
        serializer = self.serializer_class

        queryset = request.user.budget
        
        # queryset = serializers_budget.database_main_models.Budget.objects.filter(budgetUser=request.user)
        serializer = serializer(queryset, many=False)
        return Response(serializer.data)