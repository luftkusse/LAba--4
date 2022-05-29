FROM python:3.8
RUN mkdir -p /home/src/app_front
ADD requirements.txt /home/src/app_front
RUN pip install -r /home/src/app_front/requirements.txt
ADD main.py /home/src/app_front
ADD run.sh /home/src/app_front
ADD /app /home/src/app_front/app
RUN chmod +x /home/src/app_front/run.sh
ENV FLASK_APP /home/src/app_front/app/__init__.py
CMD /home/src/app_front/run.sh
