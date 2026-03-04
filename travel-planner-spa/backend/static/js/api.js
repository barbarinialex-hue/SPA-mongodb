// Punto B: LOGIN
async function handleLogin() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMsg = document.getElementById('login-error');

    if (!username || !password) {
        errorMsg.textContent = 'Inserisci username e password';
        return;
    }

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('currentUser', username);
            errorMsg.textContent = '';
            document.getElementById('login-view').style.display = 'none';
            document.getElementById('app-header').style.display = 'block';
            loadTrips();
            showView('list-view');
        } else {
            errorMsg.textContent = data.message || 'Credenziali non valide';
        }
    } catch (error) {
        console.error('Errore login:', error);
        errorMsg.textContent = 'Errore di connessione';
    }
}

// Logout
function logout() {
    localStorage.removeItem('currentUser');
    document.getElementById('app-header').style.display = 'none';
    document.getElementById('login-view').style.display = 'block';
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    showView('login-view');
}

// Punto E: Aggiungi nuovo viaggio
async function handleAddTrip() {
    const title = document.getElementById('trip-title').value;
    const destination = document.getElementById('trip-destination').value;
    const lat = parseFloat(document.getElementById('trip-lat').value) || 0;
    const lng = parseFloat(document.getElementById('trip-lng').value) || 0;
    const notes = document.getElementById('trip-notes').value;

    if (!title || !destination) {
        alert('Compila almeno titolo e destinazione');
        return;
    }

    const newTrip = {
        title,
        destination,
        coordinates: { lat, lng },
        status: 'todo',
        participants: [],
        activities: [],
        expenses: [],
        notes
    };

    try {
        const response = await fetch(`${API_URL}/trips`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newTrip)
        });

        if (response.ok) {
            document.getElementById('trip-title').value = '';
            document.getElementById('trip-destination').value = '';
            document.getElementById('trip-lat').value = '';
            document.getElementById('trip-lng').value = '';
            document.getElementById('trip-notes').value = '';
            loadTrips();
            showView('list-view');
        }
    } catch (error) {
        console.error('Errore aggiunta viaggio:', error);
    }
}

// Punto F: Aggiungi partecipante
async function addParticipant(tripId) {
    const participant = prompt('Nome partecipante:');
    if (!participant) return;

    try {
        const trip = await fetch(`${API_URL}/trips/${tripId}`).then(r => r.json());
        const participants = trip.participants || [];
        
        if (participants.includes(participant)) {
            alert('⚠️ Questo partecipante è già nella lista!');
            return;
        }
        
        participants.push(participant);

        const response = await fetch(`${API_URL}/trips/${tripId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ participants })
        });

        if (response.ok) {
            alert(`✅ ${participant} aggiunto ai partecipanti!`);
            loadTripDetail(tripId);
        }
    } catch (error) {
        console.error('Errore aggiunta partecipante:', error);
        alert('❌ Errore nell\'aggiunta del partecipante');
    }
}

// Punto G: Aggiungi attività
async function addActivity(tripId) {
    const name = prompt('Nome attività:');
    if (!name) return;
    
    const time = prompt('Orario (es: 10:00):');
    if (!time) return;
    
    try {
        const trip = await fetch(`${API_URL}/trips/${tripId}`).then(r => r.json());
        const activities = trip.activities || [];
        activities.push({ name, time });

        const response = await fetch(`${API_URL}/trips/${tripId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ activities })
        });

        if (response.ok) {
            alert(`✅ Attività "${name}" aggiunta alle ${time}!`);
            loadTripDetail(tripId);
        }
    } catch (error) {
        console.error('Errore aggiunta attività:', error);
        alert('❌ Errore nell\'aggiunta dell\'attività');
    }
}

// Punto H: Aggiungi spesa
async function addExpense(tripId) {
    const item = prompt('Descrizione spesa:');
    if (!item) return;
    
    const amountStr = prompt('Importo (€):');
    if (!amountStr) return;
    
    const amount = parseFloat(amountStr);
    if (isNaN(amount) || amount <= 0) {
        alert('❌ Inserisci un importo valido');
        return;
    }

    try {
        const trip = await fetch(`${API_URL}/trips/${tripId}`).then(r => r.json());
        const expenses = trip.expenses || [];
        expenses.push({ item, amount });

        const response = await fetch(`${API_URL}/trips/${tripId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expenses })
        });

        if (response.ok) {
            alert(`✅ Spesa di €${amount.toFixed(2)} per "${item}" aggiunta!`);
            loadTripDetail(tripId);
        }
    } catch (error) {
        console.error('Errore aggiunta spesa:', error);
        alert('❌ Errore nell\'aggiunta della spesa');
    }
}

// Punto J: Download viaggio in PDF
function downloadTrip(tripId, tripTitle) {
    try {
        fetch(`${API_URL}/trips/${tripId}/download`)
            .then(r => {
                if (!r.ok) throw new Error('Errore nel download');
                return r.blob();
            })
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${tripTitle}.pdf`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                alert(`✅ PDF "${tripTitle}.pdf" scaricato!`);
            })
            .catch(error => {
                console.error('Errore download:', error);
                alert('❌ Errore nel download del PDF');
            });
    } catch (error) {
        console.error('Errore:', error);
        alert('❌ Errore nel download');
    }
}

// Controlla login al caricamento
window.addEventListener('DOMContentLoaded', () => {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
        document.getElementById('login-view').style.display = 'none';
        document.getElementById('app-header').style.display = 'block';
        loadTrips();
    }
});
