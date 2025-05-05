import re
import json
import os
import logging
from typing import Dict, Any
from fastapi import HTTPException
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.critical("OPENAI_API_KEY environment variable is not set")
    raise RuntimeError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=OPENAI_API_KEY)

async def text_to_json(text: str) -> Dict[str, Any]:
    """Transform prompt to json using OpenAI API"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract structured data from the following text and format as valid JSON with these fields: query (string), near (string), price (float), open_now (boolean = True or False). All of the fields are required."
                    )
                },
                {"role": "user", "content": text},
            ],
        )
       
        content = response.choices[0].message.content
        
        # Extract JSON from the response
        match = re.search(r"```json\s*({[\s\S]*?})\s*```", content)
        if not match:
            match = re.search(r"({[\s\S]*?})", content)
        
        if not match:
            logger.warning(f"Could not extract JSON from OpenAI response: {content}")
            raise ValueError("JSON object not found in response.")

        parsed_json = json.loads(match.group(1))
        
        # Validate required fields
        if not parsed_json.get("query"):
            raise ValueError("Query is required")
        if not parsed_json.get("near"):
            raise ValueError("Near is required")
        if not parsed_json.get("price"):
            raise ValueError("Price is required")
        if not parsed_json.get("open_now"):
            raise ValueError("Open_now is required")
            
        return parsed_json
        
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {e}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in OpenAI response: {content}")
        raise HTTPException(status_code=500, detail="Failed to parse event data")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error generating event: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")