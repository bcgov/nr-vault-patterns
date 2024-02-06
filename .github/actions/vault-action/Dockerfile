FROM python

ENV VAULT_URL='https://vault-iit.apps.silver.devops.gov.bc.ca'
ENV BROKER_URL='https://nr-broker.apps.silver.devops.gov.bc.ca'
ENV HTTP_PROXY='http://test-forwardproxy.nrs.bcgov:23128'

RUN cd usr

RUN mkdir vault

WORKDIR /vault

COPY intention.json intention.json

ADD *.py .

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# CMD ["python3", "vault-main.py"]



