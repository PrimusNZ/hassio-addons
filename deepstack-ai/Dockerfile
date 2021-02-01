ARG BUILD_FROM
FROM $BUILD_FROM

ENV SLEEP_TIME 0.01
ENV CUDA_MODE False
ENV APPDIR /app
ENV VISION-SCENE True
ENV VISION-DETECTION True

RUN mkdir /deeptemp
RUN mkdir /data

ENV DATA_DIR /data
ENV TEMP_PATH /deeptemp/
ENV PROFILE desktop_cpu

WORKDIR /app
RUN pip install onnxruntime==0.4.0

RUN pip3 install redis
RUN pip3 install opencv-python
RUN pip3 install Cython
RUN pip3 install pillow
RUN pip3 install scipy
RUN pip3 install tqdm
RUN pip3 install tensorboard
RUN pip3 install PyYAML
RUN pip3 install Matplotlib

RUN apt-get update
RUN apt-get install -y golang

RUN mkdir /app/sharedfiles
COPY ./deepstack/sharedfiles/yolov5m.pt /app/sharedfiles/yolov5m.pt
COPY ./deepstack/sharedfiles/face.pt /app/sharedfiles/face.pt
COPY ./deepstack/sharedfiles/facerec-high.model /app/sharedfiles/facerec-high.model
COPY ./deepstack/sharedfiles/scene.model /app/sharedfiles/scene.model
COPY ./deepstack/sharedfiles/categories_places365.txt /app/sharedfiles/categories_places365.txt

RUN mkdir /app/server
COPY deepstack/server /app/server

RUN cd /app/server && go build

RUN apt-get autoremove -y --purge golang
RUN apt-get clean -y
RUN rm -rf /var/lib/apt/lists/*

RUN mkdir /app/intelligencelayer
COPY deepstack/intelligencelayer /app/intelligencelayer

COPY ./deepstack/init.py /app

EXPOSE 5000

WORKDIR /app/server

CMD ["/app/server/server"]
