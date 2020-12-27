from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import dataset

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates/")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse('home.html', context={'request': request})

@app.get("/api/dataset")
def read_dataset():
    return dataset.read()