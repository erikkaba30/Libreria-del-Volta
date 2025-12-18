from flask import Flask, render_template, request, redirect
import sqlite3
import os
import random

app = Flask(__name__)

# Percorso database per Render (Piano Free)
DB_PATH = '/tmp/libreria.db'

def get_db_connection():
    """Crea una connessione al database e si assicura che la tabella esista"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Crea la tabella ogni volta che ci connettiamo (se non esiste)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS libri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titolo TEXT NOT NULL,
            autore TEXT NOT NULL,
            descrizione TEXT,
            colore TEXT
        )
    ''')
    return conn

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        libri = conn.execute('SELECT * FROM libri').fetchall()
        conn.close()
        return render_template('index.html', libri=libri)
    except Exception as e:
        # Se c'è un errore, lo stampa nel terminale di Render per aiutarci
        print(f"Errore nel database: {e}")
        return "C'è stato un problema con la libreria. Prova a ricaricare la pagina."

@app.route('/aggiungi', methods=['POST'])
def aggiungi():
    titolo = request.form.get('titolo', '').strip()
    autore = request.form.get('autore', '').strip()
    descrizione = request.form.get('descrizione', '').strip()
    colore = f"hsl({random.randint(0, 360)}, 70%, 75%)"

    if titolo and autore:
        try:
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO libri (titolo, autore, descrizione, colore)
                VALUES (?, ?, ?, ?)
            ''', (titolo, autore, descrizione, colore))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Errore nel salvataggio: {e}")
            
    return redirect('/')

if __name__ == '__main__':
    # Questo serve solo per il test locale
    app.run(debug=True)
