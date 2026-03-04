from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
import io
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Collegamento Atlas
CONNECTION_STRING = "mongodb+srv://barbarini_alex:mQnMD3AtnkEhr##@cluster0.yrnn1km.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(CONNECTION_STRING)
db = client.travelDB

def parse_json(data):
    if isinstance(data, list):
        for item in data:
            item['_id'] = str(item['_id'])
    else:
        data['_id'] = str(data['_id'])
    return data

# --- ROTTA PER SERVIRE INDEX.HTML ---
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# B) LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    credentials = request.json
    user = db.users.find_one({
        "username": credentials.get('username'),
        "password": credentials.get('password')
    })
    if user:
        return jsonify({"status": "success", "user": user['username']}), 200
    return jsonify({"status": "error", "message": "Credenziali errate"}), 401

# C) ELENCO VIAGGI (e Punto I per la Mappa)
@app.route('/api/trips', methods=['GET'])
def get_trips():
    trips = list(db.trips.find())
    return jsonify(parse_json(trips))

# D) DETTAGLIO SINGOLO VIAGGIO
@app.route('/api/trips/<id>', methods=['GET'])
def get_trip(id):
    trip = db.trips.find_one({"_id": ObjectId(id)})
    if trip:
        return jsonify(parse_json(trip))
    return jsonify({"error": "Viaggio non trovato"}), 404

# E) INSERIMENTO NUOVO VIAGGIO
@app.route('/api/trips', methods=['POST'])
def add_trip():
    new_trip = request.json
    # Se mancano campi, MongoDB li accetta comunque, ma noi assicuriamoci la struttura base
    res = db.trips.insert_one(new_trip)
    return jsonify({"id": str(res.inserted_id)}), 201

# F, G, H) AGGIORNAMENTO (Partecipanti, Attività, Spese)
@app.route('/api/trips/<id>', methods=['PUT'])
def update_trip(id):
    updated_data = request.json
    db.trips.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
    return jsonify({"message": "Aggiornato con successo"})

# J) DOWNLOAD PDF
@app.route('/api/trips/<id>/download', methods=['GET'])
def download_trip(id):
    trip = db.trips.find_one({"_id": ObjectId(id)})
    
    # Crea un BytesIO per il PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=12,
        alignment=1  # center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2ca02c'),
        spaceAfter=10,
        spaceBefore=10
    )
    
    story = []
    
    # Titolo
    story.append(Paragraph(f"📍 {trip['title']}", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Informazioni base
    story.append(Paragraph("<b>Destinazione:</b> " + trip['destination'], styles['Normal']))
    story.append(Paragraph("<b>Status:</b> " + trip.get('status', 'N/A'), styles['Normal']))
    if trip.get('notes'):
        story.append(Paragraph("<b>Note:</b> " + trip['notes'], styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Partecipanti
    story.append(Paragraph("👥 Partecipanti", heading_style))
    participants = trip.get('participants', [])
    if participants:
        for p in participants:
            story.append(Paragraph(f"• {p}", styles['Normal']))
    else:
        story.append(Paragraph("Nessun partecipante", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Attività
    story.append(Paragraph("📅 Attività", heading_style))
    activities = trip.get('activities', [])
    if activities:
        activity_data = [['Attività', 'Orario']]
        for a in activities:
            activity_data.append([a.get('name', ''), a.get('time', '')])
        
        activity_table = Table(activity_data)
        activity_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ca02c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        story.append(activity_table)
    else:
        story.append(Paragraph("Nessuna attività prevista", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Spese
    story.append(Paragraph("💰 Spese", heading_style))
    expenses = trip.get('expenses', [])
    if expenses:
        expense_data = [['Descrizione', 'Importo (€)']]
        total = 0
        for e in expenses:
            amount = e.get('amount', 0)
            expense_data.append([e.get('item', ''), f"€{amount:.2f}"])
            total += amount
        
        expense_data.append([f"<b>TOTALE</b>", f"<b>€{total:.2f}</b>"])
        
        expense_table = Table(expense_data)
        expense_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d62728')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.lightblue),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT')
        ]))
        story.append(expense_table)
    else:
        story.append(Paragraph("Nessuna spesa registrata", styles['Normal']))
    
    # Costruisci il PDF
    doc.build(story)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"{trip['title']}.pdf"
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')  