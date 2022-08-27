from passlib.hash import bcrypt
from email.policy import default
from config.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, ForeignKey, Float, Boolean, create_engine
from sqlalchemy_utils import EmailType
