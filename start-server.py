import os

os.system("python -V")
# py = Path().absolute() / ".venv/Scripts/python.exe"
# print(py.exists())

os.system("start python -m deepl_fastapi_pw.run_uvicorn")
os.system("python -V")
