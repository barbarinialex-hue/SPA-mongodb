from pymongo import MongoClient

# Stringa di connessione fornita
CONNECTION_STRING = "mongodb+srv://barbarini_alex:mQnMD3AtnkEhr##@cluster0.yrnn1km.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(CONNECTION_STRING)
db = client.travelDB

# Pulizia per reset totale
db.users.drop()
db.trips.drop()

# A) Inserimento Utenti
db.users.insert_many([
    {"username": "luca", "password": "123"},
    {"username": "sara", "password": "123"},
    {"username": "admin", "password": "123"}
])

# A) Inserimento 11 viaggi aggiornati e coerenti
sample_trips = [
    {
        "title": "Weekend a Berlino",
        "destination": "Berlino",
        "coordinates": {"lat": 52.52, "lng": 13.40},
        "status": "fatto",
        "participants": ["Luca", "Sara", "Marco"],
        "activities": [{"name": "Museo di Pergamo", "time": "10:00"}, {"name": "Porta di Brandeburgo", "time": "15:00"}],
        "expenses": [{"item": "Volo", "amount": 120}, {"item": "Hotel", "amount": 200}],
        "notes": "Portare vestiti pesanti"
    },
    {
        "title": "Gita al lago",
        "destination": "Lago di Como",
        "coordinates": {"lat": 45.99, "lng": 9.24},
        "status": "da fare",
        "participants": ["Elena", "Paolo"],
        "activities": [],
        "expenses": [],
        "notes": "Picnic all'aperto"
    },
    {
        "title": "Barcellona Summer",
        "destination": "Barcellona",
        "coordinates": {"lat": 41.38, "lng": 2.17},
        "status": "fatto",
        "participants": ["Luca", "Giulia"],
        "activities": [],
        "expenses": [{"item": "Tapas", "amount": 50}, {"item": "Sagrada Familia", "amount": 30}],
        "notes": "Prenotare la spiaggia"
    },
    {
        "title": "Ski Trip",
        "destination": "Dolomiti",
        "coordinates": {"lat": 46.43, "lng": 11.86},
        "status": "da fare",
        "participants": ["Sara", "Marco", "Elena"],
        "activities": [{"name": "Sci mattutino", "time": "09:00"}],
        "expenses": [{"item": "Skipass", "amount": 55}],
        "notes": "Prenotare attrezzatura"
    },
    {
        "title": "Firenze Arte",
        "destination": "Firenze",
        "coordinates": {"lat": 43.77, "lng": 11.25},
        "status": "fatto",
        "participants": ["Luca", "Sara"],
        "activities": [{"name": "Duomo", "time": "11:00"}],
        "expenses": [{"item": "Uffizi", "amount": 20}],
        "notes": "Portare macchina fotografica"
    },
    {
        "title": "Cammino di Santiago",
        "destination": "Santiago de Compostela",
        "coordinates": {"lat": 42.88, "lng": -8.54},
        "status": "da fare",
        "participants": ["Paolo"],
        "activities": [{"name": "Tappa 1", "time": "07:00"}],
        "expenses": [],
        "notes": "Scarponi comodi"
    },
    {
        "title": "Weekend a Milano",
        "destination": "Milano",
        "coordinates": {"lat": 45.46, "lng": 9.19},
        "status": "da fare",
        "participants": ["Elena", "Giulia"],
        "activities": [{"name": "Shopping", "time": "14:00"}],
        "expenses": [{"item": "Treno", "amount": 40}],
        "notes": "Brunch in centro"
    },
    {
        "title": "Islanda Avventura",
        "destination": "Reykjavik",
        "coordinates": {"lat": 64.13, "lng": -21.90},
        "status": "fatto",
        "participants": ["Luca", "Marco"],
        "activities": [{"name": "Geysir", "time": "10:00"}],
        "expenses": [{"item": "Noleggio auto", "amount": 300}],
        "notes": "Vestiti termici"
    },
    {
        "title": "Capodanno a New York",
        "destination": "New York",
        "coordinates": {"lat": 40.71, "lng": -74.01},
        "status": "da fare",
        "participants": ["Sara", "Paolo", "Elena"],
        "activities": [],
        "expenses": [{"item": "Volo", "amount": 800}],
        "notes": "Prenotare Times Square"
    },
    {
        "title": "Safari in Kenya",
        "destination": "Masai Mara",
        "coordinates": {"lat": -1.39, "lng": 34.93},
        "status": "da fare",
        "participants": ["Marco"],
        "activities": [],
        "expenses": [],
        "notes": "Visto necessario e vaccinazioni"
    },
    {
        "title": "Road Trip California",
        "destination": "Los Angeles",
        "coordinates": {"lat": 34.05, "lng": -118.24},
        "status": "da fare",
        "participants": ["Luca", "Giulia"],
        "activities": [{"name": "Hollywood", "time": "18:00"}],
        "expenses": [{"item": "Auto", "amount": 500}],
        "notes": "Patente internazionale"
    }
]

db.trips.insert_many(sample_trips)
print(f"Successo! Database aggiornato con {len(sample_trips)} viaggi.")