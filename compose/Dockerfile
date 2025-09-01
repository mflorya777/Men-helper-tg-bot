# Stage для production сборки
FROM python:3.12-slim AS production

ARG workDir=/opt/app
WORKDIR ${workDir}

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=${workDir}

# Устанавливаем git
RUN apt-get update && apt-get install -y git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# requirements
RUN --mount=type=bind,source=./requirements.txt,target=./requirements.txt \
    pip install -r requirements.txt

COPY src ${workDir}/src
COPY main.py ${workDir}

EXPOSE 8081

CMD ["python", "./src/main.py"]

# Stage для prod сборки
FROM production AS prod

RUN --mount=type=bind,source=./requirements-dev.txt,target=./requirements-dev.txt \
    pip install -r requirements-dev.txt

COPY . ${workDir}
