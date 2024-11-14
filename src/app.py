import os
import asyncio
import logging
import aiofiles

from openai import OpenAI
from typing import Optional


# Current path
current_path = os.path.dirname(__file__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        # logging.StreamHandler()  # opcjonalnie, by logować jednocześnie do konsoli
    ]
)
logger = logging.getLogger(__name__)

# Set OpenAI key securely
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def read_file(file_path: str) -> Optional[str]:
    # Asynchronously read a text file.
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
            content = await file.read()
            logger.info("File read successfully: %s", file_path)
            return content
    except FileNotFoundError:
        logger.error("File not found: %s", file_path)
        return None
    except Exception as e:
        logger.error("Error reading file %s: %s", file_path, e)
        return None

async def process_text(text: str) -> Optional[str]:
    # Asynchronously process text using OpenAI API.
    
    system_path = os.path.relpath('../config/role.txt', current_path)  # "config/role.txt"
    user_path = os.path.relpath('../config/prompt.txt', current_path)  # "config/prompt.txt"

    system_content = await read_file(system_path)
    user_content = await read_file(user_path)

    try:
        messages = [
                {
                    "role": "system", 
                    "content": system_content
                },
                {
                    "role": "user", 
                    "content": f"{user_content}\n## File text:\n{text}"
                }
        ]

        response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=4096
        )

        answer = response.choices[0].message.content

        return answer
    except Exception as e:
        logger.error("Unexpected error during text processing: %s", e)
        return None

async def write_file(file_path: str, data: str) -> None:
    # Asynchronously write data to a text file.
    try:
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as file:
            await file.write(data)
            logger.info("File written successfully: %s", file_path)
    except Exception as e:
        logger.error("Error writing to file %s: %s", file_path, e)

async def main():
    input_path = os.path.relpath('../files/tresc_artykulu.txt', current_path)
    output_path = os.path.relpath('../files/artykul.html', current_path)

    text = await read_file(input_path)

    if text:
        result = await process_text(text)
        
        if result:
            await write_file(output_path, result)
            logger.info("Processing completed successfully.")
        else:
            logger.error("Failed to process text.")
    else:
        logger.error("Failed to read input file.")


if __name__ == "__main__":
    asyncio.run(main())
