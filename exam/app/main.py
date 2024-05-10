import uvicorn


if __name__ == '__main__':
    config = uvicorn.Config("app:app", port=8080, reload=True)
    server = uvicorn.Server(config)
    server.run()

