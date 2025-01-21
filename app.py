
from flask import Flask, render_template,send_from_directory,abort, request, redirect, url_for, session as flask_session
import os
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import scoped_session,sessionmaker
from models import Base, Flight
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base



app = Flask(__name__)
app.secret_key = 'your_secret_key'
Session = scoped_session(sessionmaker(bind=engine))
db_session = Session()

db_path = "Hotel.db"
DATABASE = 'train_copy.db'

# Helper function to connect to the Train database
def connect_db():
    return sqlite3.connect(DATABASE)

# Database setup
DATABASE_URL = "sqlite:///flights.db"
engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine


class Flight(Base):
    __tablename__ = 'flights'
    __table_args__ = {'extend_existing': True}  # Add this line

    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    origin = Column(String)
    destination = Column(String)
    depart_time = Column(DateTime)
    depart_weekday = Column(Integer)
    duration = Column(String)
    arrival_time = Column(DateTime)
    arrival_weekday = Column(Integer)
    flight_no = Column(String)
    airline_code = Column(String)
    airline = Column(String)
    economy_fare = Column(Float)
    business_fare = Column(Float)
    first_fare = Column(Float)
    check_in_baggage = Column(String)
    cabin_baggage = Column(String)
    meal = Column(String)
    cancellation = Column(String)
    origin_name = Column(String)
    destination_name = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'index': self.index,
            'origin': self.origin,
            'destination': self.destination,
            'depart_time': self.depart_time.strftime("%H:%M:%S") if self.depart_time else None,
            'depart_weekday': self.depart_weekday,
            'duration': self.duration,
            'arrival_time': self.arrival_time.strftime("%H:%M:%S") if self.arrival_time else None,
            'arrival_weekday': self.arrival_weekday,
            'flight_no': self.flight_no,
            'airline_code': self.airline_code,
            'airline': self.airline,
            'economy_fare': self.economy_fare,
            'business_fare': self.business_fare,
            'first_fare': self.first_fare,
            'check_in_baggage': self.check_in_baggage,
            'cabin_baggage': self.cabin_baggage,
            'meal': self.meal,
            'cancellation': self.cancellation,
            'origin_name': self.origin_name,
            'destination_name': self.destination_name,
        }

Session = scoped_session(sessionmaker(bind=engine))
db_session = Session()

# City names dictionary
city_names = {
    'DEL': 'Delhi (DEL)',
    'BOM': 'Mumbai (BOM)',
    'BLR': 'Bengaluru (BLR)',
    'HYD': 'Hyderabad (HYD)',
    'MAA': 'Chennai (MAA)',
    'CCU': 'Kolkata (CCU)',
    'COK': 'Kochi (COK)',
    'AMD': 'Ahmedabad (AMD)',
    'PNQ': 'Pune (PNQ)',
    'GOI': 'Goa (GOI)',
    'IXC': 'Chandigarh (IXC)',
    'ATQ': 'Amritsar (ATQ)',
    'JAI': 'Jaipur (JAI)',
    'LUH': 'Ludhiana (LUH)',
    'PAT': 'Patna (PAT)',
    'LKO': 'Lucknow (LKO)',
    'VNS': 'Varanasi (VNS)',
    'BDQ': 'Vadodara (BDQ)',
    'RPR': 'Raipur (RPR)',
    'BBI': 'Bhubaneswar (BBI)',
    'TRV': 'Thiruvananthapuram (TRV)',
    'IXR': 'Ranchi (IXR)',
    'IXJ': 'Jammu (IXJ)',
    'IXA': 'Agartala (IXA)',
    'GAU': 'Guwahati (GAU)',
    'IXZ': 'Port Blair (IXZ)',
    'IXB': 'Bagdogra (IXB)',
    'VTZ': 'Visakhapatnam (VTZ)',
    'IMF': 'Imphal (IMF)',
    'SXR': 'Srinagar (SXR)',
    'IXL': 'Leh (IXL)',
    'IXW': 'Jamshedpur (IXW)',
    'CCJ': 'Kozhikode (CCJ)',
    'IXM': 'Madurai (IXM)',
    'IXE': 'Mangalore (IXE)',
    'IXD': 'Allahabad (IXD)',
    'IXH': 'Kailashahar (IXH)',
    'IXG': 'Belgaum (IXG)',
    'IXY': 'Kandla (IXY)',
    'HJR': 'Khajuraho (HJR)',
    'ISK': 'Nashik (ISK)',
    'TIR': 'Tirupati (TIR)',
    'IXK': 'Keshod (IXK)',
    'KUU': 'Bhuntar (Kullu) (KUU)',
    'STV': 'Surat (STV)',
    'IXP': 'Pathankot (IXP)',
    'SHL': 'Shillong (SHL)',
    'VGA': 'Vijayawada (VGA)',
    'TRZ': 'Tiruchirapalli (TRZ)',
    'IXU': 'Aurangabad (IXU)',
    'RJA': 'Rajahmundry (RJA)',
    'IXN': 'Khowai (IXN)',
    'PNY': 'Pondicherry (PNY)',
    'IXG': 'Belagavi (Belgaum) (IXG)',
    'JLR': 'Jabalpur (JLR)',
    'HBX': 'Hubli (HBX)',
    'TEZ': 'Tezpur (TEZ)',
    'MYQ': 'Mysuru (MYQ)',
    'VDY': 'Vidyanagar (VDY)',
    'NAG': 'Nagpur (NAG)',
    'IXS': 'Silchar (IXS)',
    'DED': 'Dehradun (DED)',
    'ZER': 'Zero (Ziro) (ZER)',
    'UDR': 'Udaipur (UDR)',
    'IDR': 'Indore (IDR)',
    'VTZ': 'Visakhapatnam (VTZ)',
}

@app.route('/', methods=['GET', 'POST'])
def index():
    origins = db_session.query(Flight.origin).distinct().all()
    destinations = db_session.query(Flight.destination).distinct().all()

    if request.method == 'POST':

        selected_option = request.form.get('flexRadioDefault')
        selected_origin = request.form.get('origin')
        selected_destination = request.form.get('destination')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')  # 'None' if the field is optional

        flask_session['selected_trip_type'] = selected_option
        flask_session['selected_origin'] = selected_origin
        flask_session['selected_destination'] = selected_destination
        flask_session['departure_date'] = departure_date
        flask_session['return_date'] = return_date
    
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        selected_date = request.form['departure_date']

        datetime_selected_date = datetime.strptime(selected_date, "%Y-%m-%d")
        selected_weekday = datetime_selected_date.weekday()

        flights = db_session.query(Flight).filter(
            Flight.origin == origin,
            Flight.destination == destination,
            Flight.depart_weekday == selected_weekday
        ).all()

        flask_session['flights'] = [flight.to_dict() for flight in flights]

        return redirect(url_for('flight_results'))

    return render_template('index.html', origins=origins, destinations=destinations, city_names=city_names)



# ... (your existing code)

# ... (previous code)

@app.route('/fresults')
def flight_results():
    flight_ids = flask_session.get('flight_ids', [])
    # Retrieve additional values
    selected_trip_type = flask_session.get('selected_trip_type', 'Default Value')
    selected_origin = flask_session.get('selected_origin', '')
    selected_destination = flask_session.get('selected_destination', '')
    departure_date = flask_session.get('departure_date', '')
    return_date = flask_session.get('return_date', '')

    print(f"Flight IDs: {flight_ids}")
    print(f"Selected Trip Type: {selected_trip_type}")
    print(f"Selected Origin: {selected_origin}")
    print(f"Selected Destination: {selected_destination}")
    print(f"Departure Date: {departure_date}")
    print(f"Return Date: {return_date}")

    # Retrieve flight details from the database based on flight IDs
    flights = db_session.query(Flight).filter(Flight.id.in_(flight_ids)).all()

    print(f"Flights: {flights}")

    return render_template('flight_results.html', 
                           flights=flights, 
                           selected_trip_type=selected_trip_type,
                           selected_origin=selected_origin,
                           selected_destination=selected_destination,
                           departure_date=departure_date,
                           return_date=return_date)

@app.route('/fresults/<selected_origin>/<selected_destination>')
def flight_resultss(selected_origin, selected_destination):
    # Use the provided parameters to fetch flights
    datetime_selected_date = datetime.strptime(flask_session.get('departure_date', ''), "%Y-%m-%d")
    selected_weekday = datetime_selected_date.weekday()

    flights = db_session.query(Flight).filter(
        Flight.origin == selected_origin,
        Flight.destination == selected_destination,
        Flight.depart_weekday == selected_weekday
    ).all()

    # Store only flight IDs in the session
    flask_session['flight_ids'] = [flight.id for flight in flights]

    print(f"Flight IDs stored in the session: {flask_session['flight_ids']}")
    print(f"Selected Origin: {selected_origin}")
    print(f"Selected Destination: {selected_destination}")
    print(f"Selected Weekday: {selected_weekday}")
    print(f"Flights: {flights}")

    return render_template('flight_results.html', flights=flights)

# ... (rest of the code)

# ... (rest of your code)

@app.route('/hotel', methods=['GET', 'POST'])
def hotel():
    # Connect to the hotel database
    connection_hotel = sqlite3.connect(db_path)
    cursor_hotel = connection_hotel.cursor()

    # Fetch the list of cities from the database
    cursor_hotel.execute("SELECT DISTINCT City FROM Hotels")
    cities = [city[0] for city in cursor_hotel.fetchall()]

    # If the user selected a city, fetch hotels for that city, else fetch all hotels
    selected_city = request.args.get('city')
    if selected_city:
        cursor_hotel.execute("SELECT * FROM Hotels WHERE City = ?", (selected_city,))
    else:
        cursor_hotel.execute("SELECT * FROM Hotels")

    hotels = cursor_hotel.fetchall()

    # Close the hotel database connection
    connection_hotel.close()


    # Render the template with the list of hotels and city dropdown
    return render_template('hotel.html', hotels=hotels, cities=cities, selected_city=selected_city)

#triaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaal
# Add a new route to handle the search results based on location
@app.route('/search_hotels', methods=['POST'])
def search_hotels():
    # Get the selected location from the form
    city = request.form.get('city')

    # Connect to the hotel database
    connection_hotel = sqlite3.connect(db_path)
    cursor_hotel = connection_hotel.cursor()

    # Fetch hotels for the selected location
    cursor_hotel.execute("SELECT * FROM Hotels WHERE City = ?", (city,))
    hotels = cursor_hotel.fetchall()

    # Close the hotel database connection
    connection_hotel.close()

    # Render the template with the list of hotels
    return render_template('hotel_results.html', hotels=hotels)




@app.route('/book/<int:hotel_id>')
def book_hotel(hotel_id):
    # Connect to the hotel database
    connection_hotel = sqlite3.connect(db_path)
    cursor_hotel = connection_hotel.cursor()

    # Execute a query to fetch the details of the selected hotel
    cursor_hotel.execute("SELECT * FROM Hotels WHERE id = ?", (hotel_id,))
    hotel = cursor_hotel.fetchone()

    # Close the hotel database connection
    connection_hotel.close()

    # Render the template with the details of the selected hotel
    return render_template('book_hotel.html', hotel=hotel)




@app.route('/t',methods=['GET', 'POST'])
def indexx():
    # Fetch train data from the database
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM train_data')
    trains = cursor.fetchall()   
    conn.close()

    return render_template('train-first.html', trains=trains)


@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        source_station = request.form['source_station']
        destination_station = request.form['destination_station']

        conn = connect_db()  # Uses the train database
        cursor = conn.cursor()
        query = '''
         SELECT "Train No", "Train Name", "Departure Time", "Arrival Time", "Source Station Name", "Destination Station Name"
         FROM train_data
         WHERE "Source Station Name" = ? AND "Destination Station Name" = ?
          '''
        print("Executing query:", query)


        cursor.execute(query, (source_station, destination_station))
        result = cursor.fetchall()


        conn.close()

        # Store the results in the Flask session
        flask_session['trains'] = result

        return redirect(url_for('train_results'))

    return render_template('train_search.html')

@app.route('/train_results')
def train_results():
    # Retrieve train data from Flask session
    trains = flask_session.get('trains', [])

    return render_template('train_search_results.html', trains=trains)


#ABOUT page ,,,,,,
@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/waterfall.html')
def waterfall():
    return render_template('waterfall.html')

@app.route('/artforms.html')
def artforms():
    return render_template('artforms.html')

@app.route('/beaches.html')
def beaches():
    return render_template('beaches.html')

@app.route('/cuisine.html')
def cuisine():
    return render_template('cuisine.html')

@app.route('/hillstation.html')
def hillstation():
    return render_template('hillstation.html')

@app.route('/spirituality.html')
def spirituality():
    return render_template('spirituality.html')

@app.route('/unexplored.html')
def unexplored():
    return render_template('unexplored.html')

@app.route('/Falls/<waterfall_name>/<html_file>')
def waterfall_page(waterfall_name, html_file):
    directory = os.path.join('static', 'Falls', waterfall_name)
    if os.path.exists(os.path.join(directory, html_file)):
        return send_from_directory(directory, html_file)
    else:
        abort(404)

@app.route('/Cuisine/<cuisine_name>/<html_file>')
def cuisine_page(cuisine_name, html_file):
    directory = os.path.join('static', 'Cuisine', cuisine_name)
    if os.path.exists(os.path.join(directory, html_file)):
        return send_from_directory(directory, html_file)
    else:
        abort(404)

@app.route('/Spirituality/<place_name>/<html_file>')
def spirituality_page(place_name, html_file):
    directory = os.path.join('static', 'Spirituality', place_name)
    if os.path.exists(os.path.join(directory, html_file)):
        return send_from_directory(directory, html_file)
    else:
        abort(404)

@app.route('/art forms/<artform_name>/<html_file>')
def artform_page(artform_name, html_file):
    directory = os.path.join('static', 'art forms', artform_name)
    if os.path.exists(os.path.join(directory, html_file)):
        return send_from_directory(directory, html_file)
    else:
        abort(404)

@app.route('/beaches/<beach_name>/<html_file>')
def beaches_page(beach_name, html_file):
    directory = os.path.join('static', 'beaches', beach_name)
    if os.path.exists(os.path.join(directory, html_file)):
        return send_from_directory(directory, html_file)
    else:
        abort(404)

@app.route('/Hill stations/<hill_name>/<html_file>')
def hillstation_page(hill_name, html_file):
    directory = os.path.join('static', 'Hill stations', hill_name)
    if os.path.exists(os.path.join(directory, html_file)):
        return send_from_directory(directory, html_file)
    else:
        abort(404)

@app.route('/unexplored/<destination_name>/<html_file>')
def unexplored_page(destination_name, html_file):
    directory = os.path.join('static', 'unexplored', destination_name)
    if os.path.exists(os.path.join(directory, html_file)):
        return send_from_directory(directory, html_file)
    else:
        abort(404)

@app.route('/login.html') 
def login():
    return render_template('login.html')

@app.route('/gallery.html') 
def gallery():
    return render_template('gallery.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

