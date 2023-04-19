import uvicorn as uvicorn

if __name__ == '__main__':
    uvicorn.run(
        app="chat.server:app",
        host="0.0.0.0",
        port=8000,
        # reload=True
    )
