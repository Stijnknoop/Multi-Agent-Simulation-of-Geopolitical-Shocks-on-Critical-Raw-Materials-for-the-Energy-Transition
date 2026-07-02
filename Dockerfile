# 1. Gebruik een officiële en lichte Python-omgeving als basis
FROM python:3.11-slim

# 2. Zet de werkmap in de container op /app
WORKDIR /app

# 3. Kopieer eerst de requirements zodat Docker deze kan cachen (sneller bouwen)
COPY requirements.txt .

# 4. Installeer de Python-pakketjes
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kopieer de rest van de applicatiecode naar de container
COPY src/ ./src/
COPY data/ ./data/

# 6. Zorg dat de container weet waar de resultaten opgeslagen moeten worden
VOLUME /app/results

# 7. Het commando dat wordt uitgevoerd zodra de container opstart
CMD ["python", "src/main.py"]
