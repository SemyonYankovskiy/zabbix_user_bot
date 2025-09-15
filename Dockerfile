FROM python:3.13.7-alpine

ENV PYTHONOPTIMIZE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

SHELL ["/bin/sh", "-exc"]
ARG user_id=1000
ARG group_id=1001

WORKDIR /app

RUN addgroup -g $group_id appgroup \
    && adduser -D -h /app -u $user_id app $group_id \
    && chown -R $user_id:$group_id /app;

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=$user_id:$group_id . /app

USER $user_id:$group_id
STOPSIGNAL SIGINT

CMD [ "python", "main.py" ]
