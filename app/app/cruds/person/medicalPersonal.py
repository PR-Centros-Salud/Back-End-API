from models.person.medicalPersonal import MedicalPersonal, Specialization
from datetime import datetime, timedelta
from models.person.person import Person
from models.person.medicalPersonal import (
    Contract,
    Schedule,
    ScheduleDay,
    ScheduleDayAppointment,
)
from schemas.person.medicalPersonal import (
    MedicalPersonalCreate,
    MedicalPersonalGet,
    MedicalPersonalUpdate,
    ContractCreate,
    SpecializationCreate,
    SpecializationUpdate,
    ScheduleCreate,
)
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import exc, or_, and_
from validators.location import validate_location
from validators.institution import validate_institution
from validators.person.person import validate_create_person
from validators.person.medicalPersonal import (
    validate_medical_personal,
    validate_contract,
    validate_schedule_day,
    validate_schedule,
)
from cruds.person.person import delete_person
from models.institution import Institution
import os
from dotenv import load_dotenv
from twilio.rest import Client
from password_generator import PasswordGenerator
import phonenumbers

load_dotenv()


def get_medicalPersonal_contract(db, medicalPersonal_id: int, institution_id: int):
    db_medicalPersonal = validate_medical_personal(db, medicalPersonal_id)

    db_contract = (
        db.query(Contract)
        .filter(
            and_(
                Contract.medical_personal_id == medicalPersonal_id,
                Contract.institution_id == institution_id,
                Contract.status == 1,
            )
        )
        .first()
    )
    if not db_contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Personal in Institution not found",
        )
    else:
        db_schedule = (
            db.query(Schedule)
            .filter(
                and_(
                    Schedule.id == db_contract.schedule_id,
                    Schedule.status == 1,
                )
            )
            .first()
        )

        if not db_schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Schedule not found",
            )
        else:
            db_schedule_day = (
                db.query(ScheduleDay)
                .filter(
                    and_(
                        ScheduleDay.schedule_id == db_schedule.id,
                        ScheduleDay.status == 1,
                    )
                )
                .all()
            )
            db_schedule.schedule_day_list = db_schedule_day
            return db_schedule


def create_MedicalPersonal(db: Session, medicalPersonal: MedicalPersonalCreate):
    try:
        medicalPersonal = validate_create_person(db, medicalPersonal)
        db_institution = validate_institution(db, medicalPersonal.institution_id)

        num = phonenumbers.parse(medicalPersonal.phone, "BO")

        if not phonenumbers.is_valid_number(num):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number is not valid.",
            )

        if db_institution == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Institution not found",
            )

        medicalPersonal = medicalPersonal.dict()

        contract = dict()
        contract["institution_id"] = medicalPersonal.pop("institution_id")
        contract["department"] = medicalPersonal.pop("department")
        contract["role"] = medicalPersonal.pop("role")
        contract["is_lab_personal"] = medicalPersonal.pop("is_lab_personal")

        medicalPersonal["username"] = (
            medicalPersonal["email"].split("@")[0]
            + str(int(datetime.now().timestamp()))[5:]
        )
        pwo = PasswordGenerator()
        pwo.maxlen = 16
        pwo.minlen = 16
        medicalPersonal["password"] = pwo.generate()
        db_medicalPersonal = MedicalPersonal(**medicalPersonal)

        db.add(db_medicalPersonal)
        db.commit()
        db.refresh(db_medicalPersonal)

        contract["medical_personal_id"] = db_medicalPersonal.id
        db_contract = Contract(**contract)
        db.add(db_contract)
        db.commit()
        db.refresh(db_contract)

        # client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        body = (
            "\nWelcome to Medico, your account has been created successfully.\n\nYour username is: \n"
            + medicalPersonal["username"]
            + "\nand your password is: \n"
            + medicalPersonal["password"]
        )
        # message = client.messages.create(
        #     body=body, from_=os.getenv("TWILIO_NUMBER"), to=medicalPersonal["phone"]
        # )
        print(body)

    except exc.SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Medical Personal error."
        )
    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return db_medicalPersonal


def get_MedicalPersonal_by_institution(db: Session, institution_id: int):
    db_institution = validate_institution(db, institution_id)
    if db_institution != None:
        if (
            db_institution.institution_type != 3
            and db_institution.institution_type != 4
        ):
            db_medicalPersonal = (
                db.query(MedicalPersonal)
                .join(Contract)
                .filter(
                    and_(
                        Contract.institution_id == institution_id,
                        Contract.status == 1,
                    )
                )
                .all()
            )

            for medicalPersonal in db_medicalPersonal:
                medicalPersonal = medicalPersonal.__dict__
                medicalPersonal["contract"] = (
                    db.query(Contract)
                    .filter(
                        and_(
                            Contract.medical_personal_id == medicalPersonal["id"],
                            Contract.institution_id == institution_id,
                            Contract.status == 1,
                        )
                    )
                    .first()
                )
                # medicalPersonal.contract.schedule = (
                #     db.query(Schedule)
                #     .filter(
                #         and_(
                #             Schedule.id == medicalPersonal.contract.schedule_id,
                #             Schedule.status == 1,
                #         )
                #     )
                #     .first()
                # )
                # medicalPersonal.contract.schedule.schedule_day_list = (
                #     db.query(ScheduleDay)
                #     .filter(
                #         and_(
                #             ScheduleDay.schedule_id
                #             == medicalPersonal.contract.schedule_id,
                #             ScheduleDay.status == 1,
                #         )
                #     )
                #     .all()
                # )

                del medicalPersonal["_password"]
            return db_medicalPersonal
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This Institution is not valid for this operation.",
            )


def get_LabSpecialists_by_institution(db: Session, institution_id: int):
    db_institution = validate_institution(db, institution_id)
    if db_institution != None:
        if db_institution.institution_type == 1 or db_institution.institution_type == 4:
            db_medicalPersonal = (
                db.query(MedicalPersonal)
                .join(Contract)
                .filter(
                    and_(
                        Contract.institution_id == institution_id,
                        Contract.status == 1,
                        Contract.is_lab_personal == 1,
                    )
                )
                .all()
            )

            for medicalPersonal in db_medicalPersonal:
                medicalPersonal = medicalPersonal.__dict__
                del medicalPersonal["_password"]

            return db_medicalPersonal

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Institution is not valid for this operation.",
        )


def add_schedule(db: Session, medical_id: int, schedule: ScheduleCreate):
    try:
        db_institution = validate_institution(db, schedule.institution_id)
        validate_schedule(
            db,
            schedule.institution_id,
            schedule.schedule_day_list,
        )
        if db_institution != None:
            if db_institution.institution_type != 3:
                db_medicalPersonal = validate_medical_personal(db, medical_id)
                db_contract = validate_contract(db, medical_id, schedule.institution_id)

                if db_contract.schedule_id == None:
                    schedule = schedule.dict()
                    schedule_day_list = schedule.pop("schedule_day_list")
                    schedule.pop("institution_id")
                    db_schedule = Schedule(**schedule)
                    db.add(db_schedule)
                    db.commit()
                    db.refresh(db_schedule)

                    for schedule_day in schedule_day_list:
                        schedule_day["day"] = schedule_day["day"].value
                        schedule_day["schedule_id"] = db_schedule.id
                        db_schedule_day = ScheduleDay(**schedule_day)
                        db.add(db_schedule_day)
                        db.commit()
                        db.refresh(db_schedule_day)
                        start_time = datetime.strptime(
                            schedule_day["start_time"].strftime("%H:%M:%S"), "%H:%M:%S"
                        )
                        end_time = datetime.strptime(
                            schedule_day["end_time"].strftime("%H:%M:%S"), "%H:%M:%S"
                        )

                        delta = int(
                            ((end_time - start_time).seconds / 60)
                            / db_schedule.estimated_appointment_time
                        )

                        start_appointment = datetime.combine(
                            datetime.today(), schedule_day["start_time"]
                        )

                        schedule_day_appointment_list = []
                        for i in range(delta):
                            end_appointment = start_appointment + timedelta(
                                minutes=db_schedule.estimated_appointment_time
                            )
                            db_schedule_day_appointment = ScheduleDayAppointment(
                                schedule_day_id=db_schedule_day.id,
                                start_time=start_appointment.time(),
                                end_time=end_appointment.time(),
                            )
                            schedule_day_appointment_list.append(
                                db_schedule_day_appointment
                            )
                            start_appointment = end_appointment
                        db.add_all(schedule_day_appointment_list)

                    db_contract.schedule_id = db_schedule.id

                    db.commit()
                    db.refresh(db_contract)
                    return db_contract
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Medical Personal has an active schedule.",
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Institution is not valid for this operation.",
                )

    except exc.SQLAlchemyError as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Schedule error."
        )


def update_MedicalPersonal(
    db: Session, medicalPersonal: MedicalPersonalUpdate, id: int
):
    db_medicalPersonal = validate_medical_personal(db, id)

    if medicalPersonal.first_name:
        db_medicalPersonal.first_name = medicalPersonal.first_name
    if medicalPersonal.last_name:
        db_medicalPersonal.last_name = medicalPersonal.last_name
    if medicalPersonal.second_last_name:
        db_medicalPersonal.second_last_name = medicalPersonal.second_last_name
    if medicalPersonal.email:
        db_medicalPersonal.email = medicalPersonal.email
    if medicalPersonal.phone:
        db_medicalPersonal.phone = medicalPersonal.phone
    if medicalPersonal.address:
        db_medicalPersonal.address = medicalPersonal.address
    if medicalPersonal.province_id and validate_location(
        db, medicalPersonal.province_id
    ):
        db_medicalPersonal.province_id = medicalPersonal.province_id
    db.commit()
    db.refresh(db_medicalPersonal)
    return db_medicalPersonal


def remove_medicalPersonal(db: Session, medical_id: int, institution_id: int):
    db_medicalPersonal = validate_medical_personal(db, medical_id)

    db_contract = (
        db.query(Contract)
        .filter(
            and_(
                Contract.medical_personal_id == medical_id,
                Contract.institution_id == institution_id,
                Contract.status == 1,
            )
        )
        .first()
    )

    if not db_contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical Personal in Institution not found",
        )

    db_contract.status = 0
    db_contract.end_date = datetime.utcnow()
    db.commit()
    db.refresh(db_contract)
    return {"detail": "Medical Personal removed successfully"}


def get_contracts(db: Session, id: int):
    db_medicalPersonal = validate_medical_personal(db, id)

    db_contract = (
        db.query(Contract)
        .filter(
            and_(
                Contract.medical_personal_id == id,
                Contract.status == 1,
            )
        )
        .all()
    )

    for contract in db_contract:
        db_institution = (
            db.query(Institution)
            .filter(
                and_(
                    Institution.id == contract.institution_id,
                    Institution.status == 1,
                )
            )
            .first()
        )
        contract.institution = db_institution
        db_schedule = (
            db.query(Schedule)
            .filter(
                and_(
                    Schedule.id == contract.schedule_id,
                    Schedule.status == 1,
                )
            )
            .first()
        )
        if db_schedule:
            contract.schedule = db_schedule
            db_schedule_day = (
                db.query(ScheduleDay)
                .filter(
                    and_(
                        ScheduleDay.schedule_id == contract.schedule_id,
                        ScheduleDay.status == 1,
                    )
                )
                .all()
            )
            if db_schedule_day:
                contract.schedule.schedule_day_list = db_schedule_day

    return db_contract


def get_specializations(db: Session, id: int):
    db_medicalPersonal = validate_medical_personal(db, id)

    db_specializations = (
        db.query(Specialization)
        .filter(
            and_(
                Specialization.medical_personal_id == id,
                Specialization.status == 1,
            )
        )
        .all()
    )
    return db_specializations


def add_specialization(
    db: Session, specialization: SpecializationCreate, medical_id: int
):
    db_medicalPersonal = validate_medical_personal(db, medical_id)
    specialization = specialization.dict()
    specialization["medical_personal_id"] = medical_id
    db_specialization = Specialization(**specialization)
    db.add(db_specialization)
    db.commit()
    db.refresh(db_specialization)
    return db_specialization


def update_specialization(
    db: Session,
    specialization_id: int,
    specialization: SpecializationUpdate,
    medical_id: int,
):
    db_medicalPersonal = validate_medical_personal(db, medical_id)
    db_specialization = (
        db.query(Specialization)
        .filter(
            and_(
                Specialization.medical_personal_id == medical_id,
                Specialization.id == specialization_id,
                Specialization.status == 1,
            )
        )
        .first()
    )

    if not db_specialization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specialization not found",
        )

    if specialization.specialization_name:
        db_specialization.specialization_name = specialization.specialization_name
    if specialization.degree:
        db_specialization.degree = specialization.degree
    if specialization.institution:
        db_specialization.institution = specialization.institution
    if specialization.start_date:
        db_specialization.start_date = specialization.start_date
    if specialization.end_date:
        db_specialization.end_date = specialization.end_date
    if specialization.location:
        db_specialization.location = specialization.location
    db.commit()
    db.refresh(db_specialization)
    return db_specialization


def delete_specialization(db: Session, specialization_id: int, medical_id: int):
    db_medicalPersonal = validate_medical_personal(db, medical_id)
    db_specialization = (
        db.query(Specialization)
        .filter(
            and_(
                Specialization.medical_personal_id == medical_id,
                Specialization.id == specialization_id,
                Specialization.status == 1,
            )
        )
        .first()
    )

    if not db_specialization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specialization not found",
        )

    db_specialization.status = 0
    db.commit()
    db.refresh(db_specialization)
    return {"detail": "Specialization deleted successfully"}
