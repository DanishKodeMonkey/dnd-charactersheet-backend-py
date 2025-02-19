# Base Python image
FROM python:3.13

# ENV variables, real time stdout stderr to terminal
ENV PYTHONBUFFERED=1

# Workdir
WORKDIR /app

# Copy and install
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install prisma

# Copy rest of code 1-1
COPY . .

# Generate prisma client once container starts
RUN prisma generate --schema app/models/schema.prisma

CMD ["python", "main.py"]