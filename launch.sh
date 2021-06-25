#!/bin/bash
cd `dirname $0`
if [ `cat storage/disabled` -eq 1 ]
then
./run.sh
fi