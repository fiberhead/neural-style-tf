FROM nvcr.io/nvidia/tensorflow:19.06-py3

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update --fix-missing 

RUN apt-get install software-properties-common -y

RUN apt-get install -y \
    wget \
    curl \
    git \
    zip \
    vim \
    pkg-config \
    cmake \
    build-essential

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py --force-reinstall

RUN apt-get install -y \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev

RUN apt-get install -y \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev

RUN apt-get install -y libgtk-3-dev

RUN apt-get install -y \
    libatlas-base-dev \
    gfortran

RUN apt-get install -y \
    python3-numpy

RUN apt-get install -y \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libgtk2.0-dev \
    liblapack-dev \
    libswscale-dev
    
RUN apt-get clean 

RUN rm -rf /tmp/* /var/tmp/*

RUN apt-get install -y tzdata

RUN dpkg-reconfigure --frontend noninteractive tzdata

RUN apt-get install python-opencv -y


RUN pip3 install requests

RUN pip3 install Flask

RUN pip3 install scikit-image


RUN mkdir -p /src

WORKDIR /src

ADD requirements.txt /src/

RUN pip3 install -r requirements.txt

ADD app_utils.py /src/

ADD app.py /src/

ADD neural_style.py /src/

ADD styles /src/styles/

RUN pip3 install -r requirements.txt

EXPOSE 5000

#ENTRYPOINT ["python3"]

#CMD ["app.py"]
