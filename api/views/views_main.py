from api.views.views import *
from api.serializers import serializers_budget
from api.serializers import serializers_user

class dashboard(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        user = request.user
        budget = request.user.budget

        def get_new(user):
            budget = serializers_budget.database_main_models.Budget(budgetUser=user)
            budget.save()
            user = budget.budgetUser

            return (budget, user)

        now = serializers_user.serializers.timezone.now()
        if budget == None:
            budget, user = get_new(user)
        elif not (budget.budgetMonth == now.month and budget.budgetYear == now.year):
            budget, user = get_new(user)

        response = {
            'user': serializers_user.user_serializer(user, many=False).data,
            'budget': serializers_budget.budget_serializer(budget, many=False).data
        }

        return Response(response)