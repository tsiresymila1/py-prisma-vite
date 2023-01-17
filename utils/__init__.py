

import bcrypt
from starlite import UploadFile
from pathlib import Path
import os
import uuid


async def save_file(file: UploadFile, directory: str = "public/files", encrypted: bool = False):
    filename: str = file.filename
    if encrypted:
        filename = f"{uuid.uuid4().hex}.{file.filename.split('.')[-1]}"
    content: bytes = await file.read()
    open(Path(os.getcwd(),directory,filename), "wb").write(content)
    return filename

def hash_pasword(password:str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


