FROM quay.io/gaheyrich/ope:beta-ope

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN chmod 777 /app
RUN export PYTHONDONTWRITEBYTECODE=1

RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 -k gthread --threads 10 app:app --timeout 600
