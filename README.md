
# OpenAI Async File Processor

This repository contains a Python project for processing text files asynchronously using the OpenAI API. The code reads text data from input files, processes it using an OpenAI language model, and writes the output to a specified file.

## Features
- Asynchronous file I/O with `aiofiles`,
- OpenAI API integration for text processing,
- Logging to `app.log` for tracking file reads, writes, and errors.

## Prerequisites
- Python 3.7 or higher,
- An OpenAI API key. Set it as an environment variable `OPENAI_API_KEY`.

## Installation
1. Clone this repository.
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project directory.
   ```bash
   cd <project_directory>
   ```
3. Install required packages.
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
### Logging
Logs are saved to `app.log` in the root directory. Modify the logging configuration in the code if a different log location or format is needed.

### Environment Variables
Set your OpenAI API key in the environment:
```bash
export OPENAI_API_KEY="your_api_key"
```

## Usage
Run the main script:
```bash
python app.py
```

This script performs the following steps:
1. Reads text from the input file `../files/tresc_artykulu.txt`.
2. Processes the text with OpenAI's language model.
3. Writes the processed text to the output file `../files/artykul.html`.

### Testing
To test the app, use unit tests.

## Project Structure
- `main.py` - Main script to execute the file processing.
- `app.log` - Log file storing info and error logs.
- `config/role.txt` and `config/prompt.txt` - Configuration files containing prompts for the OpenAI API.

## License
This project is licensed under the MIT License.

