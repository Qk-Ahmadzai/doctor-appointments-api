from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Models
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    user_type = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    experience = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    contact_number = db.Column(db.String(100))
    address = db.Column(db.String(100))
    profile_picture_url = db.Column(db.String(100))


    def __init__(self, name, email, password, user_type,specialization, experience, qualification, contact_number, address, profile_picture_url):
      self.name = name
      self.email = email
      self.password = password
      self.user_type = user_type
      self.specialization = specialization
      self.experience = experience
      self.qualification = qualification
      self.contact_number = contact_number
      self.address = address
      self.profile_picture_url = profile_picture_url

    # Relationships
    appointments_as_doctor = db.relationship('Appointment', foreign_keys='Appointment.doctor_id', backref='doctor', lazy=True)
    appointments_as_patient = db.relationship('Appointment', foreign_keys='Appointment.patient_id', backref='patient', lazy=True)
    availabilities = db.relationship('Availability', backref='user', lazy=True)
    reviews_as_doctor = db.relationship('Review', foreign_keys='Review.doctor_id', backref='doctor', lazy=True)
    reviews_as_patient = db.relationship('Review', foreign_keys='Review.patient_id', backref='patient', lazy=True)

class Appointment(db.Model):
    appointment_id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    appointment_date = db.Column(db.DateTime)
    appointment_time = db.Column(db.DateTime)
    status = db.Column(db.String(100))
    reason_for_visit = db.Column(db.String(100))
    prescription = db.Column(db.String(100))

class Availability(db.Model):
    availability_id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    day_of_week = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(100))
    review_date = db.Column(db.DateTime)