from pydantic import BaseModel, Field, condecimal, conint
from typing import List, Optional

class ETA(BaseModel):
    station_id: int = Field(..., alias="staId")
    stop_id: int = Field(..., alias="stpId")
    station_name: str = Field(..., alias="staNm")
    stop_description: str = Field(..., alias="stpDe")
    run_number: int = Field(..., alias="rn")  # run number of train being predicted for
    route: str = Field(..., alias="rt")
    destination_stop: int = Field(..., alias="destSt")
    destination_number: str = Field(..., alias="destNm")
    train_direction: int = Field(..., alias="trDr")
    prediction: str = Field(..., alias="prdt")
    arrival_time: str = Field(..., alias="arrT")
    is_approaching: int = Field(..., alias="isApp")
    is_schedule: int = Field(..., alias="isSch")  # indicates whether this is a live prediction or based on schedule in lieu of live data
    is_delayed: int = Field(..., alias="isDly")
    is_fault: int = Field(..., alias="isFlt")  # indicates schedule fault
    flags: Optional[str] = Field(None, alias="flags")
    latitude: float| None = Field(..., alias="lat")
    longitude: float | None = Field(..., alias="lon")
    heading: str | None = Field(..., alias="heading")
    
class CTATT(BaseModel):
    time: str = Field(..., alias="tmst")
    error_code: int = Field(..., alias="errCd")
    error_number: Optional[str] = Field(None, alias="errNm")
    eta: List[ETA] = Field(..., alias="eta")