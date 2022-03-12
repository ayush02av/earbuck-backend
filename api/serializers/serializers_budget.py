from api.serializers.serializers import *
from database_main import models as database_main_models

class budget_serializer(serializers.ModelSerializer):
    class Meta:
        model = database_main_models.Budget

        fields = (
            'budgetMonth',
            'budgetYear',
            'budgetIncome',
            'budgetExpenses',
            'budgetSavings',
            'budgetGoal',
            'budgetIndex'
        )