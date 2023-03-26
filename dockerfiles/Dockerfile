FROM python:3.11-slim
WORKDIR /app/
ADD app /app/
RUN rm -rf /app/test/
ADD Pipfile* /app/
RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN pipenv install --system --ignore-pipfile
CMD ["python3", "main.py"]

