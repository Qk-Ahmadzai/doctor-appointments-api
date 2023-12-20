from flask import Blueprint, render_template, jsonify, request
from models import db, User, Appointment, Availability, Review
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

routes_app = Blueprint('routes_app', __name__)

# Create an instance of the Bcrypt class
bcrypt = Bcrypt()


@routes_app.route('/')
def index():
  return render_template('index.html')


# User Routes
# GET method for retrieving a user's information
@routes_app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
  # Find the user in the database
  user = User.query.get(user_id)

  if not user:
    return jsonify({'message': 'User not found'}), 404

  # Get the related data from other tables
  specialization = user.specialization
  experience = user.experience
  qualification = user.qualification
  appointments = [appointment.serialize() for appointment in user.appointments]
  availabilities = [
      availability.serialize() for availability in user.availabilities
  ]
  reviews = [review.serialize() for review in user.reviews]

  # Create a dictionary representation of the user and related data
  user_data = {
      'id': user.id,
      'name': user.name,
      'email': user.email,
      'user_type': user.user_type,
      'contact_number': user.contact_number,
      'address': user.address,
      'profile_picture_url': user.profile_picture_url,
      'specialization': specialization.name if specialization else None,
      'experience': experience.years if experience else None,
      'qualification': qualification.title if qualification else None,
      'appointments': appointments,
      'availabilities': availabilities,
      'reviews': reviews
  }

  # Return the user data
  return jsonify({'user': user_data}), 200


@routes_app.route('/users', methods=['POST'])
def create_user():
  data = request.get_json()
  password = data.get('password')
  hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

  new_user = User(name=data['name'],
                  email=data['email'],
                  password=hashed_password,
                  user_type=data['user_type'],
                  specialization=data['specialization'],
                  experience=data['experience'],
                  qualification=data['qualification'],
                  contact_number=data['contact_number'],
                  address=data['address'],
                  profile_picture_url=data['profile_picture_url'])
  db.session.add(new_user)
  db.session.commit()
  return jsonify({'message': 'User created successfully'}), 201


# PUT method for updating a user
@routes_app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
  # Get the user data from the request
  data = request.json

  # Find the user in the database
  user = User.query.get(user_id)

  if not user:
    return jsonify({'message': 'User not found'}), 404

    # Update the user attributes
  if data and 'name' in data:
    user.name = data['name']
  if data and 'email' in data:
    user.email = data['email']
  if data and 'user_type' in data:
    user.user_type = data['user_type']
  if data and 'specialization' in data:
    user.specialization = data['specialization']
  if data and 'experience' in data:
    user.experience = data['experience']
  if data and 'qualification' in data:
    user.qualification = data['qualification']
  if data and 'contact_number' in data:
    user.contact_number = data['contact_number']
  if data and 'address' in data:
    user.address = data['address']
  if data and 'profile_picture_url' in data:
    user.profile_picture_url = data['profile_picture_url']

  # Commit the changes to the database
  db.session.commit()

  # Return the updated user data
  return jsonify({
      'message': 'User updated successfully',
      'user': {
          'name': user.name,
          'email': user.email,
          'user_type': user.user_type,
          'specialization': user.specialization,
          'experience': user.experience,
          'qualification': user.qualification,
          'contact_number': user.contact_number,
          'address': user.address,
          'profile_picture_url': user.profile_picture_url
      }
  }), 200


# DELETE method for deleting a user
@routes_app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
  # Find the user in the database
  user = User.query.get(user_id)

  if not user:
    return jsonify({'message': 'User not found'}), 404

  # Delete the user from the database
  db.session.delete(user)
  db.session.commit()

  # Return a success message
  return jsonify({
      'message': 'User deleted successfully',
      'user': {
          'name': user.name,
          'email': user.email,
          'user_type': user.user_type,
          'specialization': user.specialization,
          'experience': user.experience,
          'qualification': user.qualification,
          'contact_number': user.contact_number,
          'address': user.address,
          'profile_picture_url': user.profile_picture_url
      }
  }), 200
