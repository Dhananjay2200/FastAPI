from fastapi import FastAPI

app = FastAPI()

all_customer = [
    {"id":101,"name":"Ravi","city":"begaluru","risk":"low"},
    {"id":102,"name":"Om","city":"mumbai","risk":"high"},
    {"id":103,"name":"Prakash","city":"mumbai","risk":"high"},
    {"id":104,"name":"Yash","city":"begaluru","risk":"medium"},
    {"id":105,"name":"Gopal","city":"delhi","risk":"medium"},
    ]

@app.get("/customers")
def get_customers(city:str,risk:str):
    filtered = [
        c for c in all_customer if c["city"] == city and c["risk"] == risk

    ]

    return {
        'city':city,
        'risk':risk,
        'count':len(filtered),
        'result':filtered
    }