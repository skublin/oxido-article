from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.utils import secure_filename
import os
import asyncio
import aiofiles
from app_api import main as process_file_main  # Importujemy funkcję main z app_api.py

# Konfiguracja aplikacji Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Potrzebne do używania flash i sesji
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt'}

# Tworzenie folderu uploads, jeśli nie istnieje
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Sprawdza czy plik ma dozwolone rozszerzenie."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Czyszczenie poprzedniego stanu sesji
        session.pop('processed_content', None)
        session.pop('file_processed', None)
        
        # Sprawdzenie obecności pliku w żądaniu
        if 'file' not in request.files:
            flash('Brak pliku w żądaniu')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Nie wybrano pliku')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Przetwarzanie pliku za pomocą istniejącej logiki z app_api.py
            try:
                asyncio.run(process_file_main(file_path))  # Używamy asyncio.run() aby uruchomić asynchroniczne przetwarzanie
            except Exception as e:
                flash(f'Błąd podczas przetwarzania tekstu przez OpenAI: {e}')
                return redirect(request.url)

            # Odczytanie przetworzonego pliku artykul.html
            processed_file_path = os.path.join(os.path.dirname(file_path), 'artykul.html')
            if not os.path.exists(processed_file_path):
                flash('Błąd: nie znaleziono przetworzonego pliku artykul.html')
                return redirect(request.url)

            with open(processed_file_path, 'r', encoding='utf-8') as f:
                processed_content = f.read()

            # Zapisanie przetworzonej treści do sesji oraz ustawienie flagi przetworzenia
            session['processed_content'] = processed_content
            session['file_processed'] = True  # Flaga, która informuje, że plik został przetworzony
            session['processed_file_path'] = processed_file_path  # Ścieżka do przetworzonego pliku
            flash('Plik został przetworzony. Możesz teraz wyświetlić artykuł.')
            return redirect(request.url)
        else:
            flash('Nieprawidłowy plik. Dozwolone są tylko pliki .txt.')
            return redirect(request.url)
    return render_template('index.html', file_processed=session.get('file_processed', False))

@app.route('/result')
def result():
    content = session.get('processed_content', '')
    if not content:
        flash('Nie znaleziono przetworzonej treści. Wczytaj plik ponownie.')
        return redirect(url_for('index'))
    return render_template('result.html', content=content)

@app.route('/download')
def download():
    processed_file_path = session.get('processed_file_path')
    if not processed_file_path or not os.path.exists(processed_file_path):
        flash('Nie znaleziono przetworzonego pliku do pobrania.')
        return redirect(url_for('index'))
    return send_file(processed_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

