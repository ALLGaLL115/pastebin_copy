FROM python

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "trash_code" ]