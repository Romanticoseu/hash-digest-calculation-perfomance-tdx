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
And I have four sets of default configurations to test
```yaml
client_config:
  type: continuous
  size: 1-100
  times_or_steps: 1
---
client_config:
  type: continuous
  size: 100-1000
  times_or_steps: 10
---
client_config:
  type: continuous
  size: 1000-10000
  times_or_steps: 100
---
client_config: 
  type: discrete 
  size: [1kb, 10kb, 100kb, 1mb, 10mb]
  times_or_steps: 10

```


### In native
We should change in workdir and use [Run two containers section](#how-to-run-containers)'s command to run.
The important thing to note is that setting the environment variable `TDX_ENABLE` to "false".
We can run the command directly without the need to build, as the image has already been pushed to Docker Hub.

We can get the result in `log/*.csv`
### In tdx
We should enter in a [tdx-vm](#tdx-vm) and make sure the vm has `Docker`
Because we have generate data file in previous step, we can use `scp` to cpy data files.
Then just set `TDX_ENABLE` as true to run the command in previous steps.
We can get the result in `log/*.csv`

## Analyze results and plot them
I use `google colab` to plot them. And you can see the result in this [link](https://drive.google.com/drive/folders/1fLGbNxuz9Rhs60zujCUf9jEzJmqjWwoN?usp=sharing)



## The tdx-vm <a name="tdx-vm"></a>
This `tdx-vm` has been deployed in our company's machine.
The process is very complicated and requires a series of hardware and BIOS configurations.
This vm use libvirt to launch and the vm manager is virsh.
