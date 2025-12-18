from flask import Flask, render_template, request, redirect
import sqlite3
import random

app = Flask(__name__)

DB_PATH = '/tmp/libreria.db'

def init_db():
    """Crea la tabella nel database se non esiste già"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS libri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titolo TEXT NOT NULL,
                autore TEXT NOT NULL,
                descrizione TEXT,
                colore TEXT
            )
        ''')


@app.route('/')
def index():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row  # Permette di accedere ai dati per nome colonna
        libri = conn.execute('SELECT * FROM libri').fetchall()
    return render_template('index.html', libri=libri)


@app.route('/aggiungi', methods=['POST'])
def aggiungi():
    titolo = request.form.get('titolo', '').strip()
    autore = request.form.get('autore', '').strip()
    descrizione = request.form.get('descrizione', '').strip()

    # Colore pastello per il dorso
    colore = f"hsl({random.randint(0, 360)}, 70%, 75%)"

    if titolo and autore:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('''
                INSERT INTO libri (titolo, autore, descrizione, colore)
                VALUES (?, ?, ?, ?)
            ''', (titolo, autore, descrizione, colore))
    return redirect('/')


if __name__ == '__main__':
    init_db()
    # '0.0.0.0' serve per rendere l'app visibile agli altri dispositivi in rete

    app.run(debug=True, host='0.0.0.0', port=5000)
