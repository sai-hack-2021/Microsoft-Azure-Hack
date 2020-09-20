# INSTALL PYTHON IMAGE
FROM iyappan24/ubuntupy

# INSTALL TOOLS
RUN apt-get update \
    && apt-get -y install unzip \
    && apt-get -y install libaio-dev


RUN mkdir backend

COPY . / /backend/

WORKDIR /backend

RUN pip3 install -r requirements.txt
RUN pip3 install -e .
RUN chmod +x boot.sh
EXPOSE 8000
CMD ["./boot.sh"]
