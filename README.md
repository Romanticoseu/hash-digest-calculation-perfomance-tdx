# Comparing Performance of Hash Digest Calculation (SHA-256) with and without TDX

## Build Image
```bash
docker build \
  --build-arg http_proxy=http://child-prc.intel.com:913/ \
  --build-arg https_proxy=http://child-prc.intel.com:913/ \
  --rm --no-cache -t romanticoseu/hash-digest-calculation-perfomance-tdx:2.4.0-SNAPSHOT .
```