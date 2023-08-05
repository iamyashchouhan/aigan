from fastapi import FastAPI, HTTPException
from PIL import Image
import io
import requests

app = FastAPI()

API_URL = "https://api-inference.huggingface.co/models/digiplay/perfectlevel10"
headers = {"Authorization": f"Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

@app.get("/generate_image/")
async def generate_image(prompt: str):
    try:
        image_bytes = query({
            "inputs": prompt,
        })

        # Convert the bytes response to PIL.Image
        image = Image.open(io.BytesIO(image_bytes))

        # Save the image to a file
        image_path = "generated_image.png"
        image.save(image_path)

        return {"message": "Image generated and saved", "image_path": image_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
