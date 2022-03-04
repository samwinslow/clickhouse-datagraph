 docker run -d -p 3000:3000 \
  --mount type=bind,source=/home/samwinslow/clickhouse-datagraph/metabase/plugins,destination=/plugins \
  --network clickhouse-datagraph_ch_network \
  --name metabase metabase/metabase
