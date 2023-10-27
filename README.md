# Comparing Performance of Hash Digest Calculation (SHA-256) with and without TDX

## Build Image
```bash
docker build \
  --build-arg http_proxy=http://child-prc.intel.com:913/ \
  --build-arg https_proxy=http://child-prc.intel.com:913/ \
  --rm --no-cache -t romanticoseu/hash-digest-calculation-perfomance:test .
```
## Generate test data
We can use the `tr` command to generate random data to transfer from A to B
And use the script:
```bash
cd data
chmod +x generate.sh
./generate.sh 1kb    # e.g., 1kb, 50kb, 100kb, 1mb, 10mb
```

## Run two containers
```bash
# create container_B
export DOCKER_IMAGE=romanticoseu/hash-digest-calculation-perfomance:test
docker run -itd \
	--cpuset-cpus="0-3" \
	--memory="2G" \
	-e http_proxy=http://child-prc.intel.com:913/ \
	-e https_proxy=http://child-prc.intel.com:913/ \
	--name zehua-test-B \
	-p 12345:12345/udp \
	$DOCKER_IMAGE \
	-m server

# create container_A
export DOCKER_IMAGE=romanticoseu/hash-digest-calculation-perfomance:test
export DATA_PATH="$(pwd)/data"
docker run -itd \
	--cpuset-cpus="4-7" \
	--memory="2G" \
	-e http_proxy=http://child-prc.intel.com:913/ \
	-e https_proxy=http://child-prc.intel.com:913/ \
	-e SERVER_HOST_NAME=zehua-test-B \
	-e DATA_PATH=/app/data/small.txt \
	-v $DATA_PATH:/app/data \
	--name zehua-test-A \
	--link zehua-test-B \
	$DOCKER_IMAGE \
	-m client
```

