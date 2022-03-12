from utility.database_utility import *

def get_timezone_month():
    return timezone.now().month

def get_timezone_year():
    return timezone.now().year
    
class Budget(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    budgetUser = models.ForeignKey(to="database_user.User", on_delete=models.CASCADE, related_name="budgetUser")

    budgetMonth = models.IntegerField(default=get_timezone_month, choices=[(month, str(month)) for month in range(1, 13)])
    budgetYear = models.IntegerField(default=get_timezone_year)

    budgetIncome = models.IntegerField(default=0)
    budgetExpenses = models.IntegerField(default=0)
    budgetSavings = models.IntegerField(default=0)

    budgetGoal = models.IntegerField(default=0)
    budgetIndex = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return f"{self.budgetUser.__str__()}'s {self.budgetMonth} month of {self.budgetYear}"

    def __get_self_update_object__(self):
        return Budget.objects.filter(id = self.id)

    def __update_details__(self, addNewIncome=0, addNewExpenses=0):

        selfUpdateObject = self.__get_self_update_object__()
        
        newIncome = self.budgetIncome + addNewIncome
        newExpenses = self.budgetExpenses + addNewExpenses
        newSavings = newIncome - newExpenses
        newIndex = newSavings / self.budgetGoal if self.budgetGoal >= 0 else 0.0

        newIndex = 1.0 if newIndex > 1.0 else newIndex
        
        selfUpdateObject.update(
            budgetIncome = newIncome,
            budgetExpenses = newExpenses,
            budgetSavings = newSavings,
            budgetIndex = newIndex,
            updated_at = timezone.now()
        )

    def __add_new_income__(self, amount = 0):
        self.__update_details__(addNewIncome=amount)

    def __add_new_expense__(self, amount = 0):
        self.__update_details__(addNewExpenses=amount)

    def save(self, *args, **kwargs):
        super(Budget, self).save(*args, **kwargs)
        try:
            updateUserObject = self.budgetUser.__get_self_update_object__()
            updateUserObject.update(
                budget = self,
                updated_at = timezone.now()
            )
        except Exception as exception:
            print(exception)

class Expense(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    expenseBudget = models.ForeignKey(to="database_main.Budget", on_delete=models.CASCADE, related_name="expenseBudget")
    expenseAmount = models.IntegerField(default=0)
    expenseSource = models.CharField(max_length=100, default="general")

    def __str__(self) -> str:
        return f"{self.expenseBudget.budgetUser.__str__()}'s {self.expenseAmount} expense in {self.expenseBudget.__str__()}"

    def save(self, *args, **kwargs):

        if self.expenseAmount <= self.expenseBudget.budgetSavings:
            super(Expense, self).save(*args, **kwargs)
            try:
                self.expenseBudget.__add_new_expense__(self.expenseAmount)
            except Exception as exception:
                print(exception)
        else:
            raise Exception("Sorry, you don't have enough funds to add this expense as a transaction")

class Income(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)

    incomeBudget = models.ForeignKey(to="database_main.Budget", on_delete=models.CASCADE, related_name="incomeBudget")
    incomeAmount = models.IntegerField(default=0)
    incomeSource = models.CharField(max_length=100, default="general")

    def __str__(self) -> str:
        return f"{self.incomeBudget.budgetUser.__str__()}'s {self.incomeAmount} income in {self.incomeBudget.__str__()}"

    def save(self, *args, **kwargs):
        super(Income, self).save(*args, **kwargs)
        try:
            self.incomeBudget.__add_new_income__(self.incomeAmount)
        except Exception as exception:
            print(exception)