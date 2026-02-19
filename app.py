from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run
from typing import Optional

from src.constants import APP_HOST, APP_PORT
from src.pipeline.prediction_pipeline import VehicleData, VehicleDataClassifier
from src.pipeline.training_pipeline import TrainingPipeline


app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DataForm:
    def __init__(self, request: Request):
        self.request = request

    async def get_vehicle_data(self):
        form = await self.request.form()

        return {
            "Gender": int(form.get("Gender")),
            "Age": int(form.get("Age")),
            "Driving_License": int(form.get("Driving_License")),
            "Region_Code": float(form.get("Region_Code")),
            "Previously_Insured": int(form.get("Previously_Insured")),
            "Annual_Premium": float(form.get("Annual_Premium")),
            "Policy_Sales_Channel": float(form.get("Policy_Sales_Channel")),
            "Vintage": int(form.get("Vintage")),
            "Vehicle_Age_lt_1_Year": int(form.get("Vehicle_Age_lt_1_Year")),
            "Vehicle_Age_gt_2_Years": int(form.get("Vehicle_Age_gt_2_Years")),
            "Vehicle_Damage_Yes": int(form.get("Vehicle_Damage_Yes")),
        }


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "vehicledata.html",
        {"request": request, "context": None},
    )


@app.get("/train")
async def train_model():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful!")
    except Exception as e:
        return Response(f"Error occurred: {e}")


@app.post("/")
async def predict(request: Request):
    try:
        form = DataForm(request)
        data_dict = await form.get_vehicle_data()

        vehicle_data = VehicleData(**data_dict)
        vehicle_df = vehicle_data.get_vehicle_input_data_frame()

        model_predictor = VehicleDataClassifier()
        prediction = model_predictor.predict(vehicle_df)[0]

        status = "Customer is likely to buy insurance" if prediction == 1 else "Customer is not likely to buy insurance"

        return templates.TemplateResponse(
            "vehicledata.html",
            {"request": request, "context": status},
        )

    except Exception as e:
        return templates.TemplateResponse(
            "vehicledata.html",
            {"request": request, "context": f"Error: {e}"},
        )


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port="8000")
