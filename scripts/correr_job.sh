#!/bin/bash
set -e
rm -rf /data/output/resultado
time hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files /app/mapreduce/mapper.py,/app/mapreduce/reducer.py \
  -input /data/input/ventas_125052834.csv \
  -output /data/output/resultado \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py"
cat /data/output/resultado/part-00000
