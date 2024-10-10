FROM python:3.11

RUN apt-get update && apt-get install -y \
  tesseract-ocr \
  libasound2-dev \
  libportaudio2 \
  libportaudiocpp0 \
  portaudio19-dev \
  python3-dev

RUN pip install --upgrade pip
RUN pip install requests discord.py pytesseract pillow aiohttp

WORKDIR /home/docker_volume

COPY . .