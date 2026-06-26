import io 
import joblib 
import pandas as pd
from fastapi import FastAPI,HTTPException,UploadFile,File
from fastapi.responses import StreamingResponse 
from pydantic import BaseModel,Field,model_validator

app = FastAPI()

features = joblib.load(r"C:\Users\Lenovo\Desktop\fastapi\House-prediction-api\house_features.joblib")
model = joblib.load(r"C:\Users\Lenovo\Desktop\fastapi\House-prediction-api\house_model.joblib")

#input schema
class HouseFeatures(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def accept_avg_field_names(cls, data):
        if isinstance(data, dict):
            data = data.copy()
            aliases = {
                "AvgRooms": "AveRooms",
                "AvgBedrms": "AveBedrms",
                "AvgOccup": "AveOccup",
            }
            for old_name, new_name in aliases.items():
                if new_name not in data and old_name in data:
                    data[new_name] = data[old_name]
        return data

    MedInc:     float = Field(gt=0,description="Media income of NeighbourHood")
    HouseAge:   float = Field(gt=0,description="Average age of hous in the block")
    AveRooms:   float = Field(gt=0,description="Average no of rooms")
    AveBedrms:  float = Field(gt=0,description="Average no of bed rooms")
    Population: float = Field(gt=0,description="Total Population")
    AveOccup:   float = Field(gt=0,description="Average no of occupation")
    Latitude:   float = Field(ge=32,le=42,description="Latitude")
    Longitude:  float = Field(ge=-125,le=130,description="Longitude")

# home 
@app.get("/")
def home():
    return {
        "message":"California house prediction api",
        "status":"running",
        "endpoint":"send post request to /predict"
    }

@app.get("/health")
def health():
    return {
        'status':'running',
        'model':'RandomForestRegressor',
        'features':features, 
        'avg_error':'$32754'
    }

# predict
@app.post('/predict')
def predict(house:HouseFeatures):
    try:
        input_data = pd.DataFrame(
            [{'MedInc':house.MedInc,
            'HouseAge':house.HouseAge,
            'AveRooms':house.AveRooms,
            'AveBedrms':house.AveBedrms,
            'Population':house.Population,
            'AveOccup':house.AveOccup,
            'Latitude':house.Latitude,
            'Longitude':house.Longitude}]
        )

        predict = model.predict(input_data)[0]
        price_usd = predict * 10000

        return {
            "predicted_price":f"${price_usd:,.0f}",
            "predicted_price_short":f"${predict:.2f} hundred thousands",
            "fidence_range":f"${price_usd - 32754:,.0f} to ${price_usd + 32754:,.0f}"

        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail = f"prediction failed:{str(e)}"
        )
    
@app.post("/predict-file")
async def predict_file(file:UploadFile=File(...)): # File(...) Dont look for value in url not in json value look into file uploaded ... means that is required 422 error async means that func may be wait for file upload so python run the code after that code
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=404,
            detail = "please upload the CSV File only"

        )
    contents = await file.read()
    #b"name",age'\nsagar
    df = pd.DataFrame(io.BytesIO(contents)) # BytesIO 

    required_columns = [
        'MedInc','HouseAge','AveRooms','AveBedrms',
        'Population','AveOccup','Latitude','Longitude'
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"These columns are missing from your file{missing_columns}"
        )
    
    if len(df) == 0:
        raise HTTPException(
            status_code=400,
            detail='The uploaded file has no data rows'
        )
    
    try:
        prediction = model.predict(df[required_columns])

        df["predicted_columns_usd"] = df["predicted_columns_usd"].apply(lambda x: f"${x:,.0f}")
        output = df.to_csv(index=False)

        return StreamingResponse(
            io.StringIO(output), #create fake file into memory
            media_type="text/csv", # that say to browser that file is csv file
            headers={ 
                "Content-Disposition":"attachment; Filename=prediciton.csv"
            }
        )
    # take the file and download in to csv StreamingResponse download in part if file is big
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail = f"Prediction failed:{str(e)}"
        )
