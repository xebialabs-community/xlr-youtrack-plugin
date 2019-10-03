
docker run \
           -v `pwd`/youtrack/data:/opt/youtrack/data \
           -v `pwd`/youtrack/conf:/opt/youtrack/conf \
           -v `pwd`/youtrack/logs:/opt/youtrack/logs \
           -v `pwd`/youtrack/backups:/opt/youtrack/backups \
           -p "9180:8080" jetbrains/youtrack:2019.1.52973
