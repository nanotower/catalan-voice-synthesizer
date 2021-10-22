# CATALAN TEXT TO SPEECH API

## About <a name = "about"></a>
This repository contains an api that transform any given text into audio with catalan native pronunciation. It uses a pre-trained model intented to use without GPU. It's the base of this project: [Reference](https://github.com/CollectivaT-dev/catotron-cpu), which is a implementation of [Tacotron2 developed by Nvidia](https://github.com/NVIDIA/tacotron2).
The api is protected by JWT and the results are cached in redis.

### Prerequisites

- [Docker](https://docs.docker.com/engine/#:~:text=Docker%20Engine%20is%20an%20open,a%20client%2Dserver%20application%20with%3A&text=APIs%20which%20specify%20interfaces%20that,interface%20(CLI)%20client%20docker%20.)
- [nvidia cuda](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html)
- [nvidia docker](https://developer.nvidia.com/blog/nvidia-docker-gpu-server-application-deployment-made-easy/)

## Usage

### Without gpu

- Step 1: build image

```
docker build -t voice-synth-cat:v1 -f Dockerfile.cpu .
```
- Step 2: Run stack
```
docker-compose up
```

- Step 3: Register user
You can use the pre-registered user skipping to the next step or jump into container "voice-synth-cat:v1" and run users registration script with a new user:
```
python user_registration.py --user_id 123 --username 'test-user' --password 'fd468069ebfc6cbb848bb673541c18ef979c6f2a2e5998481f2c524f0fb3257a'
```

- Step 4: Ask for your valid token
Copy the given "access_token" for the default user:
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"user": 1, "password":"fd468069ebfc6cbb848bb673541c18ef979c6f2a2e5998481f2c524f0fb3257a"}' \
  http://localhost:8080/token
```
Or change user and password of your registered one.


- Step 5: Ask the api voice to read your text in perfect Catalan
```
curl --location --request POST 'localhost:8080/' \
--header 'Authorization: Bearer <your token here>' \
--header 'Content-Type: application/json' \
--data-raw '{"text": ["frase de prova"]}'
```
Bear in mind that each sentence in the request array should be up to 130 characters length.
Your audio in the response is encoded as a base64 string.


### With NVIDIA gpu

- Step 1: Build the image
```
docker build -t voice-synth-cat-gpu:v1 -f Dockerfile.gpu .
```

- Step 2: Run de containers
```
docker run -d --network voice_synth_internal --rm redis redis-cli -h redis
docker run --gpus all -p 8080:8080 -v "$(pwd)"/logs:/app/logs --network voice_synth_internal -it --rm --name voice voice-synth-cat-gpu:v1
```
At this point, the process is the same as the CPU version. You can jump back to step 3 above.
You can deploy it to docker swarm too:
```
docker stack deploy --compose-file docker-stack.yml voice-synth-gpu-stack
```

### Workers
By default the api has one worker for each cpu server. This setup can be overridden by the WORKERS_PER_CORE or WEB_CONCURRENCY environment variables. The latter specify the total number of workers, no matter how many cores the server has.

### Logs
Logs can be configured in config/logging.ymlbe and ther're stored in /logs folder. 
