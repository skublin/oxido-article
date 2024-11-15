from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.utils import secure_filename

import os
import asyncio

from typing import Set, Union, IO

from app_api import main as process_file_main


# Flask app configuration:
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')    # necessary for flash and session
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS']: Set[str] = {'txt'}

# Create /uploads if not exists:
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename: str) -> bool:
    """ Checks if file extenstion is correct. """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    """ Creates route for main page, and render content. """
    if request.method == 'POST':
        # Clear previous session:
        session.pop('processed_content', None)
        session.pop('file_processed', None)
        
        if 'file' not in request.files:
            flash('File not in request.')
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            flash('File not selected.')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Use app_api to process file:
            try:
                asyncio.run(process_file_main(file_path))
            except Exception as e:
                flash(f'Error while processing with OpenAI API: {e}')
                return redirect(request.url)

            # Read processed file:
            processed_file_path = os.path.join(os.path.dirname(file_path), 'artykul.html')

            if not os.path.exists(processed_file_path):
                flash('Error: processed file not found.')
                return redirect(request.url)

            with open(processed_file_path, 'r', encoding='utf-8') as f:
                processed_content = f.read()

            # Save processed text to session and set flag:
            session['processed_content'] = processed_content
            session['file_processed'] = True
            session['processed_file_path'] = processed_file_path
            flash('File processed, ready to show article.')

            return redirect(request.url)
        else:
            flash('Incorrect file, onyl .txt extension.')
            return redirect(request.url)
        
    return render_template('index.html', file_processed=session.get('file_processed', False))

@app.route('/result')
def result() -> str:
    """ Creates route for result page with content rendered. """
    content = session.get('processed_content', '')
    if not content:
        flash('Processed content not found, send file again.')
        return redirect(url_for('index'))
    
    return render_template('result.html', content=content)

@app.route('/download')
def download() -> Union[IO, str]:
    """ Creates route for file download. """
    processed_file_path = session.get('processed_file_path')

    if not processed_file_path or not os.path.exists(processed_file_path):
        flash('Processed file to download not found.')
        return redirect(url_for('index'))
    
    return send_file(processed_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
