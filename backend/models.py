from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database import Base


# ---------------- PATIENT TABLE ----------------

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    dob = Column(String)
    gender = Column(String)
    phone = Column(String)


# ---------------- DOCTOR TABLE ----------------

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialization = Column(String)


# ---------------- APPOINTMENT TABLE ----------------

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    date = Column(String)
    token_number = Column(Integer)


# ---------------- CONSULTATION TABLE ----------------

class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    appointment_id = Column(Integer, ForeignKey("appointments.id"))

    symptoms = Column(String)
    diagnosis = Column(String)
    prescription = Column(String)
    notes = Column(String)