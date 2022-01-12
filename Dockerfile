FROM python:3.9.7-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install netcat -y

COPY src .

ARG USER=auth_api_user
RUN addgroup --system ${USER} && \
    adduser --system --no-create-home --ingroup ${USER} ${USER} && \
    chown -R ${USER}:${USER} /app
USER $USER

RUN chmod +x scripts/wait_for_dbs.sh
ENTRYPOINT ["./scripts/wait_for_dbs.sh"]
CMD ["python", "run.py"]
