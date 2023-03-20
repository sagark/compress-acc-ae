#!/usr/bin/env bash

set -ex

SSHOPTS="-o StrictHostKeyChecking=no"

THISDIR=$(pwd)
IPADDRFILE=$(pwd)/ipaddr

AWSTOOLSDIR=../../../sims/firesim/deploy/awstools

cd $AWSTOOLSDIR

python awstools.py benchlaunch 2>&1 | tee $IPADDRFILE
cd $THISDIR

# wait for instance boot
sleep 5m


IPADDR=$(grep -E -o "192\.168\.[0-9]{1,3}\.[0-9]{1,3}" $IPADDRFILE | head -n 1)

echo $IPADDR

scp $SSHOPTS -r ../software/benchmarks/HyperCompressBench/extracted_benchmarks/Snappy-* $IPADDR:
scp $SSHOPTS -r LZBENCH_DIFF $IPADDR:
scp $SSHOPTS -r runner.sh $IPADDR:
ssh $SSHOPTS $IPADDR "./runner.sh" 2>&1 | tee hyper-remoterun

scp $SSHOPTS -r $IPADDR:XEON_DECOMPRESS_RESULT intermediates/
scp $SSHOPTS -r $IPADDR:XEON_COMPRESS_RESULT intermediates/

cd $AWSTOOLSDIR
python awstools.py benchterminate

cd $THISDIR
python xeon-postprocess.py &> hyper_results/XEON_FINAL_RESULT.csv
