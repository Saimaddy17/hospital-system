from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import engine, Base, SessionLocal
import backend.models as models
from backend.schemas import (
    PatientCreate,
    PatientResponse,
    DoctorCreate,
    DoctorResponse,
    AppointmentCreate,
    AppointmentResponse
)

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


# ---------------- PATIENT APIs ----------------

@app.post("/patients", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = models.Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


@app.get("/patients", response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).all()


# ---------------- DOCTOR APIs ----------------

@app.post("/doctors", response_model=DoctorResponse)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = models.Doctor(**doctor.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor


@app.get("/doctors", response_model=list[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    return db.query(models.Doctor).all()


# ---------------- APPOINTMENT APIs ----------------

@app.post("/appointments", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(models.Patient.id == appointment.patient_id).first()
    doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctor_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    existing = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == appointment.doctor_id,
        models.Appointment.date == appointment.date
    ).count()

    token = existing + 1

    new_appointment = models.Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        date=appointment.date,
        token_number=token
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


@app.get("/appointments", response_model=list[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(models.Appointment).all()


# ---------------- QUEUE STATUS ----------------

@app.get("/queue-status")
def get_queue_status(doctor_id: int, date: str, token_number: int, db: Session = Depends(get_db)):

    appointments = db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.date == date
    ).all()

    if not appointments:
        return {
            "doctor_id": doctor_id,
            "date": date,
            "message": "No appointments yet"
        }

    current_token = min(a.token_number for a in appointments)

    patients_ahead = max(token_number - current_token, 0)

    estimated_wait_minutes = patients_ahead * 5

    return {
        "doctor_id": doctor_id,
        "date": date,
        "your_token": token_number,
        "current_token": current_token,
        "patients_ahead": patients_ahead,
        "estimated_wait_minutes": estimated_wait_minutes
    }