from models import Base
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

class Event(Base):
    """
    Represents an event.

    Attributes:
        id (int): The unique identifier of the event.
        creation_date (datetime): The date and time when the event was created.
        start_date (datetime): The start date and time of the event.
        end_date (datetime): The end date and time of the event.
        location (str): The location of the event.
        attendees_count (int): The number of attendees for the event.
        notes (str): Additional notes or description for the event.
        contract_id (int): The ID of the contract associated with the event.
        support_contact_id (int): The ID of the support contact associated with the event.
        contract (Contract): The contract associated with the event.
        support_contact (Employee): The support contact associated with the event.
    """

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    start_date = Column(DateTime())
    end_date = Column(DateTime())
    location = Column(String(50))
    attendees_count = Column(Integer())
    notes = Column(String(1000))
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    support_contact_id = Column(Integer, ForeignKey("employees.id"))

    contract = relationship("Contract")
    support_contact = relationship("Employee")

    @validates('start_date', 'end_date')
    def validate_event_dates(self, key, date_value):
        if key == 'start_date' and date_value < datetime.now():
            raise ValueError("start_date cannot be in the past")
        if key == 'end_date':
            if self.start_date and date_value < self.start_date:
                raise ValueError("end_date cannot be before start_date")
        return date_value

    @validates('attendees_count')
    def validate_attendees_count(self, key, count):
        if count < 0:
            raise ValueError("attendees_count must be positive")
        return count
