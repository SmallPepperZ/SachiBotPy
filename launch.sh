#!/bin/bash
echo "1" >> /Users/zachy/.tmp/test
cd `dirname $0`
if [ `cat storage/disabled` -eq 1 ]
then
echo "2" >> /Users/zachy/.tmp/test
./run.sh
fi