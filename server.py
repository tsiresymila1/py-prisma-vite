from dotenv import load_dotenv
from uvicorn.main import run

if __name__ == "__main__" :
    load_dotenv() 
    run("application:app", port=8000, reload=True,reload_excludes=["node_modules", "assets"])