FROM amazonlinux:2.0.20210219.0

#COPY vpn_cert/ZscalerRootCA.crt /etc/pki/ca-trust/source/anchors/
#RUN update-ca-trust
## The above is for my laptop and its vpn i have to use


RUN yum  update -y && \
 yum install  -y  python37 python3-wheel python3-pip && \
 python3.7 -m ensurepip  && \
 pip3 install --upgrade setuptools && \
 yum install shadow-utils.x86_64 -y

WORKDIR app
ADD requirements.txt requirements.txt

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


RUN groupadd -r senior -g 1000 && useradd -u 1000 -r -g senior -m -d /opt/senior -s /sbin/nologin -c "senior user" senior && \
    chmod 755 /opt/senior && \
    chown senior:senior -R /app/  && \
    chown senior:senior -R /opt/venv



USER senior:senior

RUN  pip install --trusted-host pypi.python.org  -r requirements.txt

ADD . /app

ENV FLASK_APP flaskr
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 8008


EXPOSE 8008


#RUN 	pip3 install flask-migrate --upgrade && \
#        flask db upgrade


ENTRYPOINT ["gunicorn"]
CMD [ "--bind", "0.0.0.0:8008", "flaskr:app"]
