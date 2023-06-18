from typing import Any

from pydantic import BaseModel


class FirstPage(BaseModel):
    customerName: Any | None = None
    opportunityId: Any | None = None
    projectName: Any | None = None
    lob: Any | None = None
    projectStartDate: Any | None = None
    projectEndDate: Any | None = None
    duration: Any | None = None
    planningType: Any | None = None
    month: Any | None = None
    week: Any | None = None
    designation: Any | None = None
    level: Any | None = None
    location: Any | None = None
    uniqueid: Any | None = None

    class Config:
        orm_mode = True


class CP(BaseModel):
    cpid: Any | None = None
    email: Any | None = None

    class Config:
        orm_mode = True


class GL(BaseModel):
    GLid: Any | None = None
    email: Any | None = None

    class Config:
        orm_mode = True


class RateCard(BaseModel):
    level: Any | None = None
    titles: Any | None = None
    country: Any | None = None
    year: Any | None = None
    rate: Any | None = None

    class Config:
        orm_mode = True


class CompanyRateCard(BaseModel):
    level: Any | None = None
    titles: Any | None = None
    country: Any | None = None
    year: Any | None = None
    rate: Any | None = None

    class Config:
        orm_mode = True
