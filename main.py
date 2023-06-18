# from fastapi.staticfiles import StaticFiles
import json
import os
import platform as plat
from pathlib import Path

import fastapi
import uvicorn
from fastapi import Depends, Body
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
import random

from starlette.responses import JSONResponse

import models
import schemas
from Reuse import CoreReusable

# from starlette.templating import Jinja2Templates

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.mount("/static", StaticFiles(directory="static"), name="static")


ROOT_DIR_PROJECT = Path(__file__).parent
print(ROOT_DIR_PROJECT)
if plat.system() == "Windows":
    path = str(ROOT_DIR_PROJECT) + os.sep + "templates" + os.sep
elif plat.system() == "Linux":
    path = str(ROOT_DIR_PROJECT) + os.sep + "templates"
else:
    path = str(ROOT_DIR_PROJECT) + os.sep + "templates"

templates = Jinja2Templates(directory=path)
# templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=models.engine)
get_db = models.get_db


@app.get('/')
def index():
    return fastapi.responses.RedirectResponse(url='/index', status_code=307)


@app.get("/index", response_class=RedirectResponse)
async def signin(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})
    # return RedirectResponse(url="/submit", status_code=303)


@app.post('/submit', status_code=200)
async def add_product(request: Request, customerName: str = Form(None), opportunityId: str = Form(None),
                      projectName: str = Form(None), lob: str = Form(None),
                      projectStartDate: str = Form(None), projectEndDate: str = Form(None), duration: str = Form(None),
                      planningType: str = Form(None),
                      db: Session = Depends(get_db)):
    # print(customerName)
    uniqueid = random.randint(1000000, 9999999)
    data = CoreReusable(customerName=customerName, opportunityId=opportunityId, projectName=projectName,
                        lob=lob, projectStartDate=projectStartDate, projectEndDate=projectEndDate, duration=duration,
                        planningType=planningType, uniqueid=uniqueid
                        )
    data.val(db)
    # return RedirectResponse(url="/temp/payu/form/" + txnid + "/verify_payment", status_code=303)
    # return templates.TemplateResponse("weekly.html", context={"request": request})
    # return fastapi.responses.RedirectResponse(url="/payu/form/"+txnid+"/verify_payment", status_code=307)

    if planningType == "Weekly":
        return templates.TemplateResponse("weekly.html", context={"request": request, "id": uniqueid})
    elif planningType == "Monthly":
        return templates.TemplateResponse("monthly.html", context={"request": request, "id": uniqueid})


@app.post('/monthlysubmit', status_code=200)
async def months(request: Request, payload=Body(...),
                 db: Session = Depends(get_db)):
    pay = json.dumps(payload)
    return templates.TemplateResponse("MCalculation.html", context={"request": request})


@app.post('/weeklysubmit', status_code=200, response_class=HTMLResponse)
async def weekly(request: Request, payload=Body(...), db: Session = Depends(get_db)):
    pay = json.dumps(payload)
    # print(pays)
    return templates.TemplateResponse("MCalculation.html", context={"request": request})


@app.post('/cp', status_code=200)
async def add_cp(request: schemas.CP, db: Session = Depends(get_db)):
    dp = request.dict()
    new_cp = models.CP(**dp)
    db.add(new_cp)
    db.commit()
    db.refresh(new_cp)
    return new_cp


@app.post('/gl', status_code=200)
async def add_gl(request: schemas.GL, db: Session = Depends(get_db)):
    dp = request.dict()
    new_gl = models.GL(**dp)
    db.add(new_gl)
    db.commit()
    db.refresh(new_gl)
    return new_gl


@app.post('/rc', status_code=200)
async def add_rc(request: schemas.RateCard, db: Session = Depends(get_db)):
    dp = request.dict()
    data = db.query(models.RateCard).filter(models.RateCard.titles == dp.get('titles')).filter(
        models.RateCard.country == dp.get('country')).first()
    if data is not None:
        return 'data already present'
    new_rc = models.RateCard(**dp)
    db.add(new_rc)
    db.commit()
    db.refresh(new_rc)
    return new_rc


@app.post('/crc', status_code=200)
async def add_crc(request: schemas.CompanyRateCard, db: Session = Depends(get_db)):
    dp = request.dict()
    data = db.query(models.CompanyRateCard).filter(models.CompanyRateCard.titles == dp.get('titles')).filter(
        models.CompanyRateCard.country == dp.get('country')).first()
    if data is not None:
        return 'data already present'
    new_crc = models.CompanyRateCard(**dp)
    db.add(new_crc)
    db.commit()
    db.refresh(new_crc)
    return new_crc


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
