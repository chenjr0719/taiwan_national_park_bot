FROM python:3.7
LABEL maintainer="Jacob <chenjr0719@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
    && apt install -y tesseract-ocr \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install \
    "beautifulsoup4==4.9.0" \
    "opencv-python==4.2.0.34" \
    "pytesseract==0.3.4" \
    "requests==2.23.0"

COPY . /tmp/src
RUN pip install /tmp/src && rm -rf /tmp/src


ENV DEBIAN_FRONTEND=dialog

CMD ["tnpb"]
