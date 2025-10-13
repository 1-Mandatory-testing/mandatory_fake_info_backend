from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fake_info import FakeInfo
import uvicorn

app = FastAPI(title="Fake Danish Person Data API", version="1.0")

# CORS middleware (samme som PHP header)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    raise HTTPException(status_code=404, detail="Incorrect API endpoint")

@app.get("/cpr")
def get_cpr():
    """Return a fake CPR"""
    fake = FakeInfo()
    return {"CPR": fake.cpr}

@app.get("/name-gender")
def get_name_gender():
    """Return fake first name, last name and gender"""
    fake = FakeInfo()
    return {
        "firstName": fake.first_name,
        "lastName": fake.last_name,
        "gender": fake.gender
    }

@app.get("/name-gender-dob")
def get_name_gender_dob():
    """Return fake first name, last name, gender and date of birth"""
    fake = FakeInfo()
    return {
        "firstName": fake.first_name,
        "lastName": fake.last_name,
        "gender": fake.gender,
        "birthDate": fake.birth_date
    }

@app.get("/cpr-name-gender")
def get_cpr_name_gender():
    """Return fake CPR, first name, last name and gender"""
    fake = FakeInfo()
    return {
        "CPR": fake.cpr,
        "firstName": fake.first_name,
        "lastName": fake.last_name,
        "gender": fake.gender
    }

@app.get("/cpr-name-gender-dob")
def get_cpr_name_gender_dob():
    """Return fake CPR, first name, last name, gender and date of birth"""
    fake = FakeInfo()
    return {
        "CPR": fake.cpr,
        "firstName": fake.first_name,
        "lastName": fake.last_name,
        "gender": fake.gender,
        "birthDate": fake.birth_date
    }

@app.get("/address")
def get_address():
    """Return a fake address"""
    fake = FakeInfo()
    return {"address": fake.address}

@app.get("/phone")
def get_phone():
    """Return a fake mobile phone number"""
    fake = FakeInfo()
    return {"phoneNumber": fake.phone_number}

@app.get("/person")
def get_person(n: int = Query(default=1, ge=1, le=100)):
    """Return fake person information (single or bulk 2-100)"""
    if n < 1 or n > 100:
        raise HTTPException(status_code=400, detail="Incorrect GET parameter value")
    
    if n == 1:
        fake = FakeInfo()
        return fake.get_fake_person()
    else:
        return FakeInfo.get_fake_persons(n)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)