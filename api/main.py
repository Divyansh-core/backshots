import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
import time

app = FastAPI()

# Vercel looks for folders relative to the root
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

count = 0
last_trigger = 0

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/detect")
async def detect(request: Request):
    global count, last_trigger
    data = await request.json()
    loudness = data.get("loudness", 0)
    result = None

    if loudness > 50 and (time.time() - last_trigger) > 1.2:
        last_trigger = time.time()
        count += 1
        # Random logic
        if count % 2 == 0:
            result = "sound" + str(random.randint(1, 2))
        else:
            result = "sound1"

    return JSONResponse({"play": result})