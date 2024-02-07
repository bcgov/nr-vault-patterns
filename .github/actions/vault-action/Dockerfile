FROM python

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV VAULT_URL='https://vault-iit.apps.silver.devops.gov.bc.ca'
ENV BROKER_URL='https://nr-broker.apps.silver.devops.gov.bc.ca'
ENV HTTP_PROXY='http://test-forwardproxy.nrs.bcgov:23128'

COPY intention.json  /usr/bin/intention.json

COPY vault-main.py /usr/bin/vault-main.py

COPY entrypoint.sh  /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]