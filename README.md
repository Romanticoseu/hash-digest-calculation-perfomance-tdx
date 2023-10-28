# Comparing Performance of Hash Digest Calculation (SHA-256) with and without TDX

## Prepare Envrionment

### Build Image
```bash
docker build \
  --build-arg http_proxy=http://child-prc.intel.com:913/ \
  --build-arg https_proxy=http://child-prc.intel.com:913/ \
  --rm --no-cache -t romanticoseu/hash-digest-calculation-perfomance:test .
```

### Generate test data
We can use the `tr` command to generate random data to transfer from A to B
And use the script:
```bash
cd data
chmod +x generate.sh
./generate.sh 1kb    # e.g., 1kb, 50kb, 100kb, 1mb, 10mb
```
Then we will mount this directory to the docker container. 

<a name="how-to-run-containers"></a>
### How to Run two containers 
```bash
# create container_B
export LOG_PATH="$(pwd)/log"
export DOCKER_IMAGE=romanticoseu/hash-digest-calculation-perfomance:test
docker run -itd \
	--cpuset-cpus="0-15" \
	--memory="16G" \
	-e http_proxy=http://child-prc.intel.com:913/ \
	-e https_proxy=http://child-prc.intel.com:913/ \
	-e TDX_ENABLE=false \
	-v $LOG_PATH:/app/log \
	--name zehua-test-B \
	-p 12345:12345/udp \
	$DOCKER_IMAGE \
	-m server

# create container_A
export DOCKER_IMAGE=romanticoseu/hash-digest-calculation-perfomance:test
export DATA_PATH="$(pwd)/data"
export LOG_PATH="$(pwd)/log"
docker run -itd \
	--cpuset-cpus="16-31" \
	--memory="16G" \
	-e http_proxy=http://child-prc.intel.com:913/ \
	-e https_proxy=http://child-prc.intel.com:913/ \
	-e SERVER_HOST_NAME=zehua-test-B \
	-e DATA_PATH=/app/data \
	-e TDX_ENABLE=false \
	-v $LOG_PATH:/app/log \
	-v $DATA_PATH:/app/data \
	--name zehua-test-A \
	--link zehua-test-B \
	$DOCKER_IMAGE \
	-m client
```

## Change configuration and test

### config
I will use the `client/config.yaml`
And I have two sets of default configurations to test
1. 
```yaml
client_config:
  type: continuous
  size: 1-100
  times: 1
```

2. 
```yaml
client_config: 
  type: discrete 
  size: [1kb, 10kb]
  times: 10
```

And I can change these configurations as appropriate

### In native
We should change in workdir and use [Run two containers section](#how-to-run-containers)'s command to run.
The important thing to note is that setting the environment variable `TDX_ENABLE` to "false".
We can run the command directly without the need to build, as the image has already been pushed to Docker Hub.

### In tdx
We should enter in a [tdx-vm](#tdx-vm) and make sure the vm has `Docker`
Then just set `TDX_ENABLE` as true to run the command in previous steps.

## Analyze results and plot them



## The tdx-vm <a name="tdx-vm"></a>