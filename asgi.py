from app.main import app

# This allows running the app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("asgi:app", host="0.0.0.0", port=8000, reload=True) 