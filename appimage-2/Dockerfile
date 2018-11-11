FROM ubuntu:trusty
ENV DEBIAN_FRONTEND=noninteractive
RUN printf '#!/bin/sh\nset -x; apt-get update -qqy && apt-get install -qqy "$@"' >install.sh && chmod +x install.sh
# Build environment.
RUN ./install.sh \
	    build-essential \
	    ccache \
	    wget \
	    ;
# For AppImage support.
RUN ./install.sh \
	    fuse \
	    libfuse2 \
	    ;
# For building Python 3.5.
RUN ./install.sh \
	    libbz2-dev \
	    libgdbm-dev \
	    liblzma-dev \
	    libncurses5-dev \
	    libreadline-dev \
	    libsqlite3-dev \
	    libssl-dev \
	    zlib1g-dev \
	    ;
# For building cython-hidapi.
RUN ./install.sh \
	    libudev-dev \
	    libusb-1.0-0-dev \
	    ;
# For building dbus-python.
RUN ./install.sh \
	    libdbus-1-dev \
	    libdbus-glib-1-dev \
	    ;
# For PyQt5.
RUN ./install.sh \
	    libasound2 \
	    libegl1-mesa \
	    libfontconfig1 \
	    libgl1-mesa-glx \
	    libnss3 \
	    libxcomposite1 \
	    libxcursor1 \
	    libxi6 \
	    libxrandr2 \
	    libxss1 \
	    libxtst6 \
	    ;
# Newer gcc.
RUN ./install.sh software-properties-common
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test
RUN apt-get remove -y software-properties-common
RUN apt-get autoremove -y
RUN ./install.sh gcc-8
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 60
# Cleanup after ourselves...
RUN rm install.sh
RUN apt-get clean
