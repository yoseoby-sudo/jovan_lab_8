FROM python:3.11-slim

WORKDIR /app

COPY systems_abstract.py inventory.json ./

CMD ["python", "-u", "systems_abstract.py"]