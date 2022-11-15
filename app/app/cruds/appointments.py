from models.appointments import Appointment, MedicalAppointment, LaboratoryAppointment
from models.institution import Room
from validators.institution import validate_institution
from models.location import Province
from schemas.appointments import AppointmentGet, AppointmentCreate, AppointmentUpdate, MedicalAppointmentFinished, LaboratoryAppointmentFinished, MedicalAppointmentCreate, LaboratoryAppointmentCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from validators.location import validate_location
from validators.person.medicalPersonal import validate_contract
from validators.appointments import validate_appointment
from cruds.person.person import delete_person
from models.person.medicalPersonal import ScheduleDay
from schemas.person.person import PersonGet
from typing import Union
from datetime import date, timedelta
from models.person.client import Client
from models.person.medicalPersonal import ScheduleDayAppointment
from models.laboratoryService import LaboratoryService
from models.person.medicalPersonal import MedicalPersonal, Contract, Schedule, ScheduleDay, ScheduleDayAppointment

def create_medical_appointment(db: Session, appointment: Union[MedicalAppointmentCreate, LaboratoryAppointmentCreate]):
    try:
        institution = validate_institution(db, appointment.institution_id)
        contract = validate_contract(
            db, appointment.medical_personal_id, appointment.institution_id
        )

        if contract.is_lab_personal and type(appointment) == MedicalAppointmentCreate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can't schedule a medical appointment with a laboratory specialist",
            )

        day = appointment.programmed_date.weekday() + 1
        db_schedule_day = (
            db.query(ScheduleDay)
            .filter(
                and_(
                    ScheduleDay.schedule_id == contract.schedule_id,
                    ScheduleDay.day == day,
                    ScheduleDay.status == 1,
                )
            )
            .first()
        )

        if not db_schedule_day:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medical Personal does not work on this day",
            )

        if validate_appointment(db, appointment, contract.schedule_id, db_schedule_day):
            if type(appointment) == MedicalAppointmentCreate:
                db_appointment = MedicalAppointment(
                    patient_id=appointment.patient_id,
                    medical_personal_id=appointment.medical_personal_id,
                    institution_id=appointment.institution_id,
                    schedule_day_appointment_id=appointment.schedule_day_appointment_id,
                    programmed_date=appointment.programmed_date,
                    room_id=db_schedule_day.room_id,
                )
                db.add(db_appointment)
                db.commit()
                db.refresh(db_appointment)
                return db_appointment
            else:
                db_laboratory_service = (
                    db.query(LaboratoryService)
                    .filter(
                        and_(
                            LaboratoryService.id == appointment.laboratory_service_id,
                            LaboratoryService.status == 1,
                        )
                    )
                    .first()
                )
                db_appointment = LaboratoryAppointment(
                    patient_id=appointment.patient_id,
                    medical_personal_id=appointment.medical_personal_id,
                    institution_id=appointment.institution_id,
                    schedule_day_appointment_id=appointment.schedule_day_appointment_id,
                    programmed_date=appointment.programmed_date,
                    room_id=db_laboratory_service.room_id,
                    laboratory_service_id=appointment.laboratory_service_id
                )
                db.add(db_appointment)
                db.commit()
                db.refresh(db_appointment)
                return db_appointment
                

    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

def update_appointment(db: Session, id: int, appointment_status: int, user: PersonGet, type: int):
    try:
        db_appointment = None

        if type == 1:
            db_appointment = db.query(MedicalAppointment).filter(
                and_(MedicalAppointment.id == id)
            ).first()
        else:
            db_appointment = db.query(LaboratoryAppointment).filter(
                and_(LaboratoryAppointment.id == id)
            ).first()

        if not db_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
            )

        if appointment_status == 2 and user.id != db_appointment.medical_personal_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You don't have permission to confirm this appointment",
            )

        if appointment_status == 2 and db_appointment.status == 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This appointment has already been confirmed",
            )

        if appointment_status == 2 and (db_appointment.status == 3 or db_appointment.status == 4): 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This appointment has cannot be confirmed again",
            )

        if appointment_status == 3 and db_appointment.status == 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This appointment has already been finished",
            )

        if appointment_status == 3 and db_appointment.status == 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This appointment has already been canceled",
            )


        if appointment_status == 3 and user.id != db_appointment.patient_id and user.id != db_appointment.medical_personal_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You don't have permission to cancel this appointment",
            )

        db_appointment.status = appointment_status
        db.commit()
        db.refresh(db_appointment)
        return db_appointment
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

def finish_appointment(db: Session, id: int, user: PersonGet, finished : Union[MedicalAppointmentFinished, LaboratoryAppointmentFinished]):
    try:
        db_appointment = None 

        if type(finished) == MedicalAppointmentFinished:
            db_appointment = db.query(MedicalAppointment).filter(
                and_(MedicalAppointment.id == id)
            ).first()
        else: 
            db_appointment = db.query(LaboratoryAppointment).filter(
                and_(LaboratoryAppointment.id == id)
            ).first()

        if not db_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
            )

        if db_appointment.status == 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This appointment has already been finished",
            )

        if db_appointment.status == 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This appointment has already been canceled",
            )
        

        if user.id != db_appointment.medical_personal_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You don't have permission to finish this appointment",
            )

        # if date.today() < db_appointment.programmed_date:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="You can't finish an appointment before the programmed date",
        #     )

        db_appointment.status = 4

        if type(finished) == MedicalAppointmentFinished:
            print('B')
            if (finished.recipe):
                print('A')
                db_appointment.medical_appointment_recipe = finished.recipe
        else:
            db_appointment.laboratory_delivery_date = finished.delivery_datetime

            if (finished.result):
                db_appointment.laboratory_results_resume = finished.result

        db.commit()
        db.refresh(db_appointment)
        return db_appointment
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

def get_appointment(db: Session, user: int, id: int, type: int):
    try:
        db_appointment = None

        if type == 0:
            db_appointment = db.query(MedicalAppointment).filter(
                and_(MedicalAppointment.id == id, or_(MedicalAppointment.patient_id == user, MedicalAppointment.medical_personal_id == user))
            ).first()
        else:
            db_appointment = db.query(LaboratoryAppointment).filter(
                and_(LaboratoryAppointment.id == id, or_(LaboratoryAppointment.patient_id == user, LaboratoryAppointment.medical_personal_id == user))
            ).first()

            db_appointment.laboratory_service = db.query(LaboratoryService).filter(
                LaboratoryService.id == db_appointment.laboratory_service_id,
            ).first()

        if not db_appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
            )

        db_appointment.medical_personal = db.query(MedicalPersonal).filter(
            MedicalPersonal.id == db_appointment.medical_personal_id,
        ).first()

        db_appointment.patient = db.query(Client).filter(
            Client.id == db_appointment.patient_id,
        ).first()

        db_appointment.room = db.query(Room).filter(
            Room.id == db_appointment.room_id,
        ).first()

        db_appointment.schedule_day_appointment = db.query(ScheduleDayAppointment).filter(
            ScheduleDayAppointment.id == db_appointment.schedule_day_appointment_id,
        ).first()

        

        return db_appointment
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

def get_medical_personal_appointments(db: Session, medical_personal_id: int, appointment_status: int, type:int):
    try:
        db_appointments = None
        if appointment_status < 1 or appointment_status > 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status"
            )
        if type == 1:
            if appointment_status == 5:
                db_appointments = db.query(MedicalAppointment).filter(
                    MedicalAppointment.medical_personal_id == medical_personal_id
                ).all()
                print(db_appointments)
            elif appointment_status == 6:
                db_appointments = db.query(MedicalAppointment).filter(
                    and_(
                        MedicalAppointment.medical_personal_id == medical_personal_id,
                        MedicalAppointment.status == 2, 
                        MedicalAppointment.programmed_date == date.today()
                    )
                ).all()
            else:
                db_appointments = (
                    db.query(MedicalAppointment)
                    .filter(
                        and_(
                            MedicalAppointment.medical_personal_id == medical_personal_id,
                            MedicalAppointment.status == appointment_status,
                        )
                    )
                    .all()
                )
            
            for appointment in db_appointments:
                appointment.patient = db.query(Client).filter(Client.id == appointment.patient_id).first()
                appointment.room = db.query(Room).filter(Room.id == appointment.room_id).first()
                appointment.schedule_day_appointment = db.query(ScheduleDayAppointment).filter(ScheduleDayAppointment.id == appointment.schedule_day_appointment_id).first()

            return db_appointments
        else:
            if appointment_status == 5:
                db_appointments = db.query(LaboratoryAppointment).filter(
                    LaboratoryAppointment.medical_personal_id == medical_personal_id
                ).all()
            elif appointment_status == 6:
                db_appointments = db.query(LaboratoryAppointment).filter(
                    and_(
                        LaboratoryAppointment.medical_personal_id == medical_personal_id,
                        LaboratoryAppointment.status == 2, 
                        LaboratoryAppointment.programmed_date == date.today()
                    )
                ).all()
            else:
                db_appointments = (
                    db.query(LaboratoryAppointment)
                    .filter(
                        and_(
                            LaboratoryAppointment.medical_personal_id == medical_personal_id,
                            LaboratoryAppointment.status == appointment_status,
                        )
                    )
                    .all()
                )

            for appointment in db_appointments:
                appointment.patient = db.query(Client).filter(Client.id == appointment.patient_id).first()
                appointment.room = db.query(Room).filter(Room.id == appointment.room_id).first()
                appointment.schedule_day_appointment = db.query(ScheduleDayAppointment).filter(ScheduleDayAppointment.id == appointment.schedule_day_appointment_id).first()
                appointment.laboratory_service = db.query(LaboratoryService).filter(LaboratoryService.id == appointment.laboratory_service_id).first()
            
            return db_appointments
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

def get_client_appointments(db: Session, patient_id: int, q: str, type: int):
    try:
        if type == 1:
            db_appointments = (
                    db.query(MedicalAppointment)
                    .filter(
                        and_(
                            MedicalAppointment.patient_id == patient_id,
                            MedicalAppointment.status == 1,
                            MedicalAppointment.programmed_date >= date.today(),
                        )
                    )
                    .all()
                )

            if q == 1:
                db_appointments = (
                    db.query(MedicalAppointment)
                    .filter(
                        and_(
                            MedicalAppointment.patient_id == patient_id,
                            MedicalAppointment.status == 2,
                            MedicalAppointment.programmed_date >= date.today(),
                        )
                    )
                    .all()
                )

                for ap in db_appointments:
                    ap.room = db.query(Room).filter(Room.id == ap.room_id).first()

            elif q == 2:
                db_appointments = (
                    db.query(MedicalAppointment)
                    .filter(
                        and_(
                            MedicalAppointment.patient_id == patient_id,
                            MedicalAppointment.status == 4,
                            MedicalAppointment.programmed_date < date.today(),
                        )
                    )
                    .all()
                )
                for ap in db_appointments:
                    ap.room = db.query(Room).filter(Room.id == ap.room_id).first()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid query"
                )
            return db_appointments
        else:
            db_appointments = (
                    db.query(LaboratoryAppointment)
                    .filter(
                        and_(
                            LaboratoryAppointment.patient_id == patient_id,
                            LaboratoryAppointment.status == 1,
                            LaboratoryAppointment.programmed_date >= date.today(),
                        )
                    )
                    .all()
                )

            if q == 1:
                db_appointments = (
                    db.query(LaboratoryAppointment)
                    .filter(
                        and_(
                            LaboratoryAppointment.patient_id == patient_id,
                            LaboratoryAppointment.status == 2,
                            LaboratoryAppointment.programmed_date >= date.today(),
                        )
                    )
                    .all()
                )

            elif q == 2:
                db_appointments = (
                    db.query(LaboratoryAppointment)
                    .filter(
                        and_(
                            LaboratoryAppointment.patient_id == patient_id,
                            LaboratoryAppointment.status == 4,
                            LaboratoryAppointment.programmed_date < date.today(),
                        )
                    )
                    .all()
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid query"
                )
            return db_appointments
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )

def get_available_times(db: Session, doctor_id : int, date_time : date):
    try:
        db_contract = db.query(Contract).filter(Contract.medical_personal_id == doctor_id).first()
        db_schedule = db.query(Schedule).filter(Schedule.id == db_contract.schedule_id).first()

        if db_schedule is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
            )

        print(type(date_time))
        db_schedule_day = db.query(ScheduleDay).filter(and_(
            ScheduleDay.day == (date_time.weekday() + 1),
            ScheduleDay.schedule_id == db_schedule.id
        )).first()
        if db_schedule_day is not None:
            db_schedule_day_appointment = db.query(ScheduleDayAppointment).filter(ScheduleDayAppointment.schedule_day_id == db_schedule_day.id).all()

            available_schedule_day = []

            for schedule_day_appointment in db_schedule_day_appointment:
                app = db.query(Appointment).filter(and_(
                    Appointment.schedule_day_appointment_id == schedule_day_appointment.id,
                    Appointment.programmed_date == date_time
                )).first()

                if app is None:
                    available_schedule_day.append(schedule_day_appointment)
            
            db_schedule_day.schedule_day_appointment = available_schedule_day
        
        return db_schedule_day
    except exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data"
        )