from mqtt_rpc import mqtt_rpc

app = mqtt_rpc.MqttRpc("mytest", ["tasks"], {"hostname": "localhost"})
