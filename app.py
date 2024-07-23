from config import *
from models import Vehicle, User, Trip, Maintenance

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header,jwt_data):
    identity= jwt_data["sub"]
    return User.query.filter_by(id = identity).one_or_none()

class Register(Resource):
    def post(self):
        data = request.get_json()
        # current_user_id =get_jwt_identity()
        new_user = User(
            email = data.get("email"),
            name = data.get("name"),
            password = bcrypt.generate_password_hash(data.get("password")).decode('utf-8')
        )
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=new_user)
        return make_response({"access_token": access_token, "user":new_user.to_dict()})



class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data["password"]
        user = User.query.filter_by(email=email).first()


        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user)
            return {"access_token": access_token}, 200
        else:
            return {"message": "Invalid email or password"}, 401
        

class Vehicles(Resource):
    def get(self):
        vehicles = Vehicle.query.all()
        vehicles = [vehicle.to_dict() for vehicle in vehicles]
        return vehicles
    
    def post(self):
        
        new_vehicle = Vehicle(
            vin = request.form.get('vin'),
            make = request.form.get('make')
        )
        db.session.add(new_vehicle)
        db.session.commit()
        response = make_response(new_vehicle.to_dict(), 201, {"Content-Type":"application/json"})
        return response

    # def patch(self):
    #     updated = 
    
class Users(Resource):
    def get(self):
        users = User.query.all()
        users = [user.to_dict() for user in users]
        return users
    
    def post(self):
        data = request.get_json()
        new_user = User(
            email = data.get("email"),
            name = data.get("name"),
            password = bcrypt.generate_password_hash(data.get("password")).decode('utf-8')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success':'user created successfully'})
    
class UserByID(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        user = user.to_dict()
        return user
    
    def patch(self, id):
        user = User.query.filter_by(id=id).first()
        data = request.get_json()
        user.name = data.get("name")
        user.email = data.get("email")
        user.password = data.get("password")
        db.session.commit()
        return jsonify({"messasge": "user updated successfully"})
    
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"messasge": "user deleted successfully"})
    

class CheckLogin(Resource):
    @jwt_required()
    def get (self):
        return make_response(current_user.to_dict(), 200)
    

class Trips(Resource):
    def get(self):
        trips = Trip.query.all()
        trips = [trip.to_dict() for trip in trips]
        return trips
     
    def post(self):
        data = request.get_json()
        new_trip = Trip(
           user_id = data['user_id'],
           vehicle_id = data['vehicle_id'],
           destination = data['destination'],
           date = data['date']
        )
        db.session.add(new_trip)
        db.session.commit()
        return make_response(new_trip.to_dict(), 200)
    
class TripsbyDestination(Resource):
    def get(self, destination):
        trips = Trip.query.filter_by(destination = destination).all()
        trips = [trip.to_dict() for trip in trips]
        return trips
    
class TripsByID(Resource):
    def get(self, id):
        trip = Trip.query.filter_by(id=id).first()
        if trip:
            trip = trip.to_dict()
            return trip,200
        return {"error":"Trip not found"}, 404
    
    def patch(self, id):
        trip = Trip.query.filter_by(id=id).first()
        if trip:
            data = request.get_json()
            trip.user_id = data.get("user_id")
            trip.vehicle_id = data.get("vehicle_id")
            trip.destination = data.get("destination")
            trip.date = data.get("date")
            db.session.commit()
            return jsonify({"message": "Trip updated successfully"})
        return {"error": "Trip not found"}
    
    def delete(self, id):
        trip = Trip.query.filter_by(id=id).first()
        if trip:
            db.session.delete(trip)
            db.session.commit()
            return jsonify({"message": "Trip deleted successfully"})
        return {"error": "Trip not found"}, 404
    
class Maintenances(Resource):
    def get(self):
        records = Maintenance.query.all()
        records = [record.to_dict() for record in records]
        return records
    
    def post(self):
        data = request.get_json()
        new_record = Maintenance(
            vehicle_id=data.get('vehicle_id'),
            user_id=data.get('user_id'),
            date=data.get('date'),
            maintenance_type = data.get("maintenance_type")
        )
        db.session.add(new_record)
        db.session.commit()
        return{"sucess": "Maintenance record created successfully"}

api.add_resource(Trips, '/trips')
api.add_resource(TripsbyDestination, '/trips/<string:destination>')
api.add_resource(TripsByID, '/trips/<int:id>')
api.add_resource(Register, '/register')   
api.add_resource(Login, '/login')
api.add_resource(CheckLogin, '/check_login')
api.add_resource(Users, '/users')
api.add_resource(UserByID, '/users/<int:id>')
api.add_resource(Vehicles, '/vehicles')
api.add_resource(Maintenances, '/maintenances')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

