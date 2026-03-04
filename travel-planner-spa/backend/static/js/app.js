const API_URL = `${window.location.protocol}//${window.location.host}/api`;

// Variabili globali per il viaggio corrente
let currentTripId = null;
let currentTripTitle = null;

// Funzione per cambiare vista (Logica SPA)
function showView(viewId) {
    document.querySelectorAll('.view').forEach(v => v.style.display = 'none');
    document.getElementById(viewId).style.display = 'block';
}

async function loadTrips() {
    const container = document.getElementById('trips-container');
    const response = await fetch(`${API_URL}/trips`);
    const trips = await response.json();
    container.innerHTML = "";

    trips.forEach(trip => {
        const card = document.createElement('div');
        card.className = 'trip-card';
        card.innerHTML = `
            <h3>${trip.title}</h3>
            <p>📍 ${trip.destination}</p>
            <button onclick="loadTripDetail('${trip._id}')">Vedi Dettaglio</button>
        `;
        container.appendChild(card);
    });
}

// Punto D, F, G, H: Carica i dettagli di un singolo viaggio
async function loadTripDetail(tripId) {
    const detailContainer = document.getElementById('trip-content');
    const response = await fetch(`${API_URL}/trips/${tripId}`);
    const trip = await response.json();

    // Salva ID e titolo per altre operazioni
    currentTripId = tripId;
    currentTripTitle = trip.title;

    const totaleSpese = trip.expenses ? trip.expenses.reduce((sum, exp) => sum + exp.amount, 0) : 0;

    detailContainer.innerHTML = `
        <h1>${trip.title}</h1>
        <p><strong>Destinazione:</strong> ${trip.destination}</p>
        <p><strong>Status:</strong> ${trip.status}</p>
        <p><strong>Note:</strong> ${trip.notes || 'Nessuna nota'}</p>
        <hr>
        
        <h3>👥 Partecipanti (Punto F)</h3>
        <ul>${trip.participants && trip.participants.length > 0 ? 
            trip.participants.map(p => `<li>${p}</li>`).join('') : 
            '<li>Nessun partecipante</li>'}
        </ul>
        <button onclick="addParticipant(currentTripId)" class="action-btn">➕ Aggiungi Partecipante</button>

        <h3>📅 Attività (Punto G)</h3>
        <ul>${trip.activities && trip.activities.length > 0 ? 
            trip.activities.map(a => `<li>${a.name} - ${a.time}</li>`).join('') : 
            '<li>Nessuna attività prevista</li>'}
        </ul>
        <button onclick="addActivity(currentTripId)" class="action-btn">➕ Aggiungi Attività</button>

        <h3>💰 Spese e Riepilogo (Punto H)</h3>
        <ul>${trip.expenses && trip.expenses.length > 0 ? 
            trip.expenses.map(e => `<li>${e.item}: €${e.amount}</li>`).join('') : 
            '<li>Nessuna spesa registrata</li>'}
        </ul>
        <button onclick="addExpense(currentTripId)" class="action-btn">➕ Aggiungi Spesa</button>
        <p><strong>TOTALE COSTI: €${totaleSpese}</strong></p>
        <hr>
        <button onclick="downloadTrip(currentTripId, currentTripTitle)" class="download-btn">📄 Scarica Info</button>
    `;

    showView('detail-view');
}

window.onload = loadTrips;