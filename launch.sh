#!/bin/bash
echo "1" >> $HOME/.tmp/test
cd `dirname $0`
if [ `cat storage/disabled` -eq 1 ]
then
echo "2" >> $HOME/.tmp/test
./run.sh
fi