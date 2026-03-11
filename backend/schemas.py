from pydantic import BaseModel


class PatientCreate(BaseModel):
    name: str
    dob: str
    gender: str
    phone: str


class PatientResponse(BaseModel):
    id: int
    name: str
    dob: str
    gender: str
    phone: str

    class Config:
        from_attributes = True


class DoctorCreate(BaseModel):
    name: str
    specialization: str


class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str

    class Config:
        from_attributes = True


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    date: str


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date: str
    token_number: int

    class Config:
        from_attributes = True