from flask import Flask, jsonify
from routes import routes_app
from models import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctor_appointment.db'
db.init_app(app)

# Register the routes from routes.py to the main app
app.register_blueprint(routes_app)
  
if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(host='0.0.0.0', debug=True)
