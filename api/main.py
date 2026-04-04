import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
import time

app = FastAPI()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

count = 0
last_trigger = 0

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # This is the exact fix for the "unhashable type: dict" error
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

@app.post("/detect")
async def detect(request: Request):
    global count, last_trigger
    data = await request.json()
    loudness = data.get("loudness", 0)
    result = None

    if loudness > 40 and (time.time() - last_trigger) > 1.2:
        last_trigger = time.time()
        count += 1
        # Random logic
        if count % 2 == 0:
            result = "sound" + str(random.randint(1, 2))
        else:
            result = "sound1"

    return JSONResponse({"play": result})
