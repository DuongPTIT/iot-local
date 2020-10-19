Artical about Kafka vs Mqtt intergration
https://www.confluent.io/blog/iot-streaming-use-cases-with-kafka-mqtt-confluent-and-waterstream/


Mqtt proxy for Kafka documentation
https://docs.confluent.io/current/kafka-mqtt/index.html

Waterstream documentation
https://waterstream.io/

Mqtt python client example
https://github.com/eclipse/paho.mqtt.python/blob/master/examples/client_pub-wait.py

Hướng dẫn cấu hình và sử dụng Kafka Connect:


Chạy file docker-compose hệ thống bao gồm: Zookeeper, Kafka, Kafka Connect, MariaDB
```bash
docker-compose -f docker-compose.yml up -d
```
Sử dụng Postman sử dụng các API được Kafka Connect publish

Hiển thị list các Connector đã được đăng ký:
```bash
GET IP:8083/connectors/
```
Kiểm tra Trạng thái của Connector đã đăng ký (check log,…):
```bash
GET IP:8083/connectors/CONNECTOR_NAME/status
```
Xoá Connector:
```bash
DELETE IP:8083/connectors/CONNECTOR_NAME
```

Đăng ký Connector:
```bash
POST IP:8083/connectors/

Body:
{
  "name": "jdbc-sink-withkey-4",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "connection.url": "jdbc:mysql://mariadb:3306/iot",
    "topics": "topic6",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "true",
    "connection.user": "root",
    "connection.password": "rootpass",
    "auto.create": true,
    "auto.evolve": true,
    "insert.mode": "insert"
  }
}
```
