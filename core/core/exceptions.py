class ExpenseNotFoundException(Exception):
    def __init__(self, expense_id: int | None = None, message: str | None = None):
        self.expense_id = expense_id
        if message:
            self.message = message
        elif expense_id is not None:
            self.message = f"Expense with id {expense_id} not found"
        else:
            self.message = "Expense not found"
        super().__init__(self.message)
