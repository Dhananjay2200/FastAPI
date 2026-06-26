from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoanApplication(BaseModel):
    age:int
    income:float
    loan_amout:float
    employment_year:float

@app.post("/predict")
def predict(application:LoanApplication):
    if application.income > 50000 and application.employment_year > 2:
        decision = "approved"
    else:
        decision = "rejected"
    
    return {
        "application_age":application.age,
        "decision":decision
    }

@ app.get("/customer/{customer_id}")
def get_customer(customer_id:int):
    return {
        "customer_id":customer_id
    }