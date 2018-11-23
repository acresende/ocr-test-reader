#!/usr/bin/env bash
# bash strict mode : http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail
IFS=$'\n\t'

LEPTONICA="leptonica-1.74.4.tar.gz"
TESSERACT="tesseract-master.tar.gz"
TESSERACT_MODEL="por.traineddata"
TESSERACT_MODEL2="eng.traineddata"

if [ ! -d ./temp ]; then
    mkdir ./temp
fi

#gogo
if [ ! -f ./temp/${LEPTONICA} ]; then
    echo "leptonica not found, downloading tarball"
    curl -L -o ./temp/${LEPTONICA} http://www.leptonica.org/source/leptonica-1.74.4.tar.gz 
fi

if [ ! -f ./temp/${TESSERACT} ]; then
    echo "tesseract not found, downloading tarball"
    curl -L -o ./temp/${TESSERACT} https://github.com/tesseract-ocr/tesseract/archive/master.tar.gz
fi 

if [ ! -f ./temp/${TESSERACT_MODEL} ]; then
    echo "tessseract model not found, downloading"
    curl -L -o ./temp/${TESSERACT_MODEL} https://github.com/tesseract-ocr/tessdata/raw/master/por.traineddata
fi

if [ ! -f ./temp/${TESSERACT_MODEL2} ]; then
    echo "tessseract model not found, downloading"
    curl -L -o ./temp/${TESSERACT_MODEL2} https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata
fi

echo "building docker container"
docker build -t "dbmobilelife/docker-python-opencv-tesseract"  .