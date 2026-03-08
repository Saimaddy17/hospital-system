from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend.database import engine, Base, SessionLocal
import backend.models
from backend.schemas import PatientCreate, PatientResponse, DoctorCreate, DoctorResponse

app = FastAPI(title="Hospital System API")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Hospital System Backend Running Successfully"}


# PATIENT APIs

@app.post("/patients", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = backend.models.Patient(
        name=patient.name,
        dob=patient.dob,
        gender=patient.gender,
        phone=patient.phone
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@app.get("/patients", response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(backend.models.Patient).all()
    return patients


# DOCTOR APIs

@app.post("/doctors", response_model=DoctorResponse)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = backend.models.Doctor(
        name=doctor.name,
        specialization=doctor.specialization
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


@app.get("/doctors", response_model=list[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    doctors = db.query(backend.models.Doctor).all()
    return doctors