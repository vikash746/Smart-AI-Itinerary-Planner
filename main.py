from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import uvicorn

# ✅ Gemini API Key
GEMINI_API_KEY = ""
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Use supported model name (update based on list_models output)
MODEL_NAME = "models/gemini-1.5-pro"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "Smart Itinerary Chatbot is running!"}

@app.post("/generate")
async def generate_itinerary(request: Request):
    data = await request.json()
    destination = data.get("destination")
    days = data.get("days", 1)
    interests = data.get("interests", [])
    start_date = data.get("start_date")

    prompt = (
        f"Create a {days}-day travel itinerary for {destination}, starting on {start_date}. "
        f"The traveler is interested in: {', '.join(interests)}. "
        f"Include sightseeing, food, local culture, and realistic daily schedules."
    )

    try:
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(prompt)
        return {"plan": response.text}
    except Exception as e:
        return {"error": str(e)}
