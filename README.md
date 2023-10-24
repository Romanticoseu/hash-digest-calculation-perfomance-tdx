# Comparing Performance of Hash Digest Calculation (SHA-256) with and without TDX

## Build Image
```bash
docker build \
  --build-arg http_proxy=http://child-prc.intel.com:913/ \
  --build-arg https_proxy=http://child-prc.intel.com:913/ \
  --rm --no-cache -t romanticoseu/hash-digest-calculation-perfomance-tdx:test .
```

## Run two containers
```bash
export DOCKER_IMAGE=romanticoseu/hash-digest-calculation-perfomance-tdx:test
# create container_A
docker run -itd \
	-e http_proxy=http://child-prc.intel.com:913/ \
	-e https_proxy=http://child-prc.intel.com:913/ \
	--name zehua-test-A \
	$DOCKER_IMAGE a

# create container_B
docker run -itd \
	-e http_proxy=http://child-prc.intel.com:913/ \
	-e https_proxy=http://child-prc.intel.com:913/ \
	--name zehua-test-B \
	$DOCKER_IMAGE b

```