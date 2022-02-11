FROM python

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY start.sh /start.sh 
RUN chmod +x /start.sh
CMD /start.sh