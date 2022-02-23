export DIRECTORY="/home/ch/datasets/aviation/normalized"

for f in $DIRECTORY/*.csv; do
  clickhouse-client --query "insert into aviation.accidents_incidents_all format CSVWithNames" < $f
done
