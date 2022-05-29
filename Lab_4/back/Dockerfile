FROM python:3.8
RUN mkdir -p /home/src/app_back
ADD requirements.txt /home/src/app_back
RUN pip install -r /home/src/app_back/requirements.txt
ADD run.sh /home/src/app_back
ADD /app /home/src/app_back/app
ADD main.py /home/src/app_back

RUN chmod +x /home/src/app_back/run.sh
ENV FLASK_APP /home/src/app_back/app/__init__.py
CMD /home/src/app_back/run.sh

