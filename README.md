run the following commands: 

python -m venv .venv

.venv\Scripts\Activate.ps1

pip install -r requirements.txt

uvicorn src.app.main:app --port 8009