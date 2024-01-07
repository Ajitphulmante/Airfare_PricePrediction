from flask import Flask, request, jsonify,render_template
import pickle
import pandas as pd
from datetime import datetime 

app = Flask(__name__)

model = pickle.load(open("regFile.pkl","rb"))

# print(model.predict([[0, 27, 4, 17, 10, 19, 40, 2, 30, False, False, False, False,
#         False, False, False, True, False, False, False, False, False,
#         False, True, False, False, False, False, False, False, True,
#         False, False]]))

headers = {"Content-Type": "application/json; charset=utf-8"}

@app.route("/")
def home():
    return render_template("index.html",name=home)

@app.route("/predict",methods=['POST'])
def predict():
    data = request.json['data']
    print("data:",data)

    # <!-- 'Total_Stops', 'Journey_day', 'Journey_month', 'Dep_hour',
    #    'Dep_minute', 'Arrival_hour', 'Arrival_minute', 'Duration_hour',
    #    'Duration_minute', 'Airline_Air India', 'Airline_GoAir',
    #    'Airline_IndiGo', 'Airline_Jet Airways', 'Airline_Jet Airways Business',
    #    'Airline_Multiple carriers',
    #    'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
    #    'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
    #    'Chennai', 'Delhi', 'Kolkata', 'Mumbai', 'Cochin', 'Delhi', 'Hyderabad',
    #    'Kolkata', 'New Delhi' -->

    details_obj = {
          "Total_Stops" : 0,
          "Journey_day" : 0,
          "Journey_month" : 0,                                    
          "Dep_hour" : 0,
          "Dep_minute" : 0,
          "Arrival_hour" : 0,
          "Arrival_minute" : 0,
          "Duration_hour" : 0,
          "Duration_minute" : 0,
          "Airline_Air India" : 0,
          "Airline_GoAir" : 0,
          "Airline_IndiGo" : 0,
          "Airline_Jet Airways" : 0,
          "Airline_Jet Airways Business" : 0,
          "Airline_Multiple carriers" : 0,
          "Airline_Multiple carriers Premium economy" : 0,
          "Airline_SpiceJet" : 0,
          "Airline_Trujet" : 0,
          "Airline_Vistara" : 0,
          "Airline_Vistara Premium economy" : 0,
          "Chennai" : 0,
          "Delhi" : 0,
          "Kolkata" : 0,
          "Mumbai" : 0,
          "Cochin" : 0,
          "Delhi1" : 0,
          "Hyderabad" : 0,
          "Kolkata1" : 0,
          "New Delhi" : 0
    }

    details_obj["Total_Stops"] = data["noOfStops"]
    details_obj[data["source"]]=1
    details_obj[data["destination"]]=1
    details_obj["Journey_day"] = pd.to_datetime(data["Date"]).day
    details_obj["Journey_month"] = pd.to_datetime(data["Date"]).month
    details_obj["Dep_hour"] =  pd.to_datetime(data["DepartureTime"]).hour
    details_obj["Dep_minute"] =  pd.to_datetime(data["DepartureTime"]).minute
    details_obj["Arrival_hour"] =  pd.to_datetime(data["ArrivalTime"]).hour
    details_obj["Arrival_minute"] =  pd.to_datetime(data["ArrivalTime"]).minute

    time1 = datetime.strptime(data["DepartureTime"], "%H:%M") 
    time2 = datetime.strptime(data["ArrivalTime"], "%H:%M") 

    time_diff = time2 - time1 

    minutes = divmod(time_diff.seconds, 60) 



    details_obj["Duration_hour"] =  minutes[0]/60
    details_obj["Duration_minute"] =  minutes[0]%60

    print(details_obj["Duration_hour"]," ",details_obj["Duration_minute"])

    details_obj[data["AirLine"]] = 1


    features = []

    print("len:",len(details_obj))

    for key in details_obj:
        print(key,end=" ")
        features.append(details_obj[key])
    
    print("features : ",features)

    AirFare = model.predict([features])

    print("Airfare:",AirFare," ",type(list(AirFare)))
    





    return list(AirFare)
    
# if(__name__=='main'):
#     app.run(debug=True)
