from datetime import datetime


class User:
    def __init__(self, user_id, email, full_name, password, role):
        self.user_id = user_id
        self.email = email
        self.full_name = full_name
        self.password = password
        self.role = role
        self.registered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.user_id,
            "email": self.email,
            "full_name": self.full_name,
            "password": self.password,
            "role": self.role,
            "registered_at": self.registered_at
        }


class Service:
    def __init__(self, service_id, service_name, price, duration, available_slots=None):
        self.service_id = service_id
        self.service_name = service_name
        self.price = price
        self.duration = duration
        self.available_slots = available_slots or []

    def to_dict(self):
        return {
            "service_id": self.service_id,
            "service_name": self.service_name,
            "price": self.price,
            "duration": self.duration,
            "available_slots": self.available_slots
        }


class Booking:
    def __init__(self, booking_id, client_name, client_email, service_name, appointment_time):
        self.booking_id = booking_id
        self.client_name = client_name
        self.client_email = client_email
        self.service_name = service_name
        self.appointment_time = appointment_time
        self.status = "Booked"

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "client_name": self.client_name,
            "client_email": self.client_email,
            "service_name": self.service_name,
            "appointment_time": self.appointment_time,
            "status": self.status
        }