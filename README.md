
# Oxido Article Generator

This repository contains a Python project for processing text files asynchronously using the OpenAI API. It's a Flask web application, created with the help of AI. The code reads text data from a given file, processes it using an OpenAI language model, writes the output to a specified file, and shows a dedicated page with the results.

## Installation
1. Clone this repository.
   ```bash
   git clone https://github.com/skublin/oxido-article
   ```
2. Navigate to the project directory.
   ```bash
   cd oxido-article
   ```
3. It is recommended to create (**and activate**) virtual environment.
   ```bash
   python -m venv venv
   ```
   ```bash
   source venv/bin/activate    # Windows: .\venv\Scripts\activate
   ```
4. Install required packages.
   ```bash
   pip install -r requirements.txt
   ```
5. Set your OpenAI API key in the environment.
   ```bash
   export OPENAI_API_KEY="your_api_key"    # Windows: set OPENAI_API_KEY="your_api_key"
   ```
6. Set any secret key.
   ```bash
   export SECRET_KEY="your_secret_key"    # Windows: set SECRET_KEY="your_secret_key"
   ```
7. Start the Flask application.
   ```bash
   python app.py
   ```
8. Open a web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Usage
This application performs the following steps:
1. Runs a Flask web app with a simple user interface.
2. Allows the user to upload a text file (only `.txt` extension is accepted).
3. Reads the uploaded file and processes it with the OpenAI API.
4. Uses a GPT-4 model to generate an HTML version of the text file (based on the role and prompt specified in the configuration).
5. Displays the generated HTML content on the result page, allowing the user to view or download the article.
6. Logs important information to `app.log` while the app is running.

## Project Structure
- `app.py` - Main script to run the Flask web application.
- `app_api.py` - Script for file processing (open, write, interact with OpenAI API, etc).
- `app.log` - Log file storing information and error logs.
- `config/role.txt` and `config/prompt.txt` - Configuration files containing prompts for the OpenAI API.
- `templates/index.html` and `templates/result.html` - Flask template files containing HTML for the main and result pages.
- `uploads/` - Folder where user-uploaded files are stored. This folder already contains an example file `tresc_artykulu.txt`.
- `files/` - Folder to check results (Oxido recruitment), there are files `artykul.html` (generated HTML article file), `szablon.html` (styled HTML file, without body) and `podglad.html` (file with generated article in styled HTML file).

## Prerequisites
- Python 3.7 or later is recommended.
- An OpenAI API key to authenticate with the OpenAI service.

## Configuration
- Ensure that you have properly set up the OpenAI API key in your environment. You can use `export OPENAI_API_KEY="your_api_key"` or set it directly in your IDE environment settings.
- The configuration files in the `config` directory (`role.txt` and `prompt.txt`) allow you to define the role and prompt used by the OpenAI model to generate the HTML output.

## Running the Application
After running `app.py`, the application will be available locally at [http://127.0.0.1:5000/](http://127.0.0.1:5000/). You can interact with the web interface to:
1. Upload a `.txt` file containing the article text.
2. Click "Send" to process the file.
3. After processing, you can view the result using the "Show Article" button.
4. Additionally, you can download the processed article in HTML format by clicking the "Download Article" button.

## Logging
- The application logs relevant information, such as upload attempts, processing status, and any errors that occur during the process.
- Logs are stored in the `app.log` file, which can be helpful for debugging or tracking the usage of the application.

## Example Workflow
1. Upload a `.txt` file (e.g., `tresc_artykulu.txt` located in the `uploads/` folder).
   
   <img width="512" alt="main_page" src="https://github.com/user-attachments/assets/ed774f9e-0c20-45db-8d6a-9f410272ba76">
   
3. The file will be processed, and the generated HTML will be displayed on the result page.
   
   <img width="512" alt="show_article_1" src="https://github.com/user-attachments/assets/8e1fb227-ff67-4077-a25b-74bfe5da35e5">
   
5. You can either view the HTML directly in the browser or download it for further use.
   
   <img width="512" alt="show_article_2" src="https://github.com/user-attachments/assets/78ea979f-3891-4ebf-8515-9d0ff82caf0f">
   

## License
This project is licensed under the MIT License.
