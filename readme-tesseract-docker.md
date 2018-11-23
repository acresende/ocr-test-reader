# Docker python opencv tesseract

Builds upon the `docker-python-opencv` image, and adds bleeding edge tesseract ocr version 4.

Installs the python [`pytesseract` package](https://pypi.python.org/pypi/pytesseract/0.1) as well as it's unlisted dependency pillow

## Building and pushing the image

Ensure that you have the following local dependencies installed:
 - `curl`
 - Docker version 1.13 RC3 or newer (as the new `--squash` flag is used)

Then Use the bundled `build.sh` script.

```
$ ./build.sh
```

ON MASTER when the build is good, you can publish to dockerhub
```
$ docker push dbmobilelife/docker-python-opencv-tesseract
```

If you get authentication problems, ensure that you are logged in
```
$ docker login
```