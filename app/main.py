from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import dataset
import os
import pandas as pd

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates/")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse('home.html', context={'request': request})

@app.get("/api/dataset")
def read_dataset():
    return dataset.read()

@app.get("/api/dataset/{dataset_name}")
def read_data(dataset_name: str):  
    df = pd.read_csv("data/"+dataset_name)
    json = df.to_json(orient='records')
    return json

@app.post("/api/dataset")
async def upload_dataset(file: UploadFile = File(...)):
    content = await file.read()
    with open("data/"+file.filename,'wb+') as f:
        f.write(content)
        f.close()
    return {"filename": file.filename,"content_type": file.content_type}
    

@app.delete("/api/dataset/{dataset_name}")
def delete_dataset(dataset_name: str):
    os.remove("data/"+dataset_name)
    return(dataset_name+" removed")