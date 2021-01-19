FROM python:3.7

COPY ./backend/requirements.txt /tmp/requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

CMD ["/bin/bash"]