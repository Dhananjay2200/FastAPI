from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoanApplication(BaseModel):
    name:str
    age:int
    income:float
    loan_amount:float
    employeement_years:int

@app.post('/predict')
def predict_loan(app:LoanApplication):
    # model logic

    approved = (
        app.income>50000 and
        app.employeement_years > 2 and
        app.age >= 21
    )

    return {
        "application name":app.name,
        "loan amount":app.loan_amount,
        "decision":"approved" if approved else "reject",
        "reviewed income": app.income
    }