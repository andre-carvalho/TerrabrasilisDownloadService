# To build image for this dockerfile use this command:
#   docker build -t shpExportService -f environment/Dockerfile .
#
# To run without compose but with shell terminal use this command:
#   docker run -p 5000:5000 -v $PWD/shp/export/service/src:/server -it shpExportService sh
#
# To run without compose and without shell terminal use this command:
#   docker run -p 5000:5000 -v $PWD/shp/export/service/src:/server shpExportService
#
#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM python:3.5-alpine

LABEL "br.inpe.dpi"="INPE/DPI-Terrabrasilis" \
br.inpe.dpi.terrama="microservice" \
version="0.1" \
author="Andre Carvalho" \
author.email="carvalho@dpi.inpe.br" \
description="This microservice receive one table name \
and other related parameters, export geodata for a shapefile and provide \
access of those shapefiles over a REST API."

ENV PYTHONUNBUFFERED 1
#-------------Application Specific Stuff ----------------------------------------------------

RUN apk update \
  && apk add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq \
    python-dev \
    py-pip \
    zlib-dev

ENV LIBRARY_PATH=/lib:/usr/lib

ENV INSTALL_PATH /server

COPY . $INSTALL_PATH/

# Install Python requirements
RUN pip install -r $INSTALL_PATH/requirements.txt

ENV APP_EXEC=$INSTALL_PATH/api/

EXPOSE 5000

VOLUME ["/server/api/export/shapefiles"]

WORKDIR $APP_EXEC

CMD ["python", "server.py"]
