from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def get_shipment():
    return {"message": "Shipment service is running."}
