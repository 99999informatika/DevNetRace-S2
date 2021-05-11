# make a container

cd ~/Docker/

docker build -t 5x9-devnetrace-s2 .

# init container

Make sure that you have public access http:5000 and http:8081, for example use ngrok:

$PATH/.ngrok/ngrok.yml

authtoken: $YOUR-TOKEN

tunnels:

  first-app:

    addr: 8081

    proto: http

  second-app:

    addr: 5000

    proto: http

Then start ngrok:

ngrok start --all -region $YOUR-REGION

copy the correct API datas , urls to docker-volume/config.cfg

# run the container

docker run --publish=5000:5000 --publish=8081:8081 --mount type=bind,source=/$YOUR_PATH/devnetrace_stage2/docker-volume,target=/app/volume 5x9_devnetrace_s2
