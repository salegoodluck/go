package main

import (
	"fmt"
	"time"

	"github.com/Shopify/sarama"
)

func main() {

	config := sarama.NewConfig()
	config.Producer.RequiredAcks = sarama.WaitForAll
	config.Producer.Partitioner = sarama.NewRandomPartitioner
	config.Producer.Return.Successes = true
	msg := &sarama.ProducerMessage{}
	msg.Topic = "nginx_log"
	msg.Value = sarama.StringEncoder("this is a good test,my message is zhaofan")
	client, err := sarama.NewSyncProducer([]string{"172.16.1.11:9092"}, config)
	if err != nil {
		fmt.Println("producer close err:", err)
		return
	}
	defer client.Close()

	for {
		pid, offset, err := client.SendMessage(msg)
		if err != nil {
			fmt.Println("send message failed,", err)
			return
		}
		fmt.Printf("pid:%v offset:%v\n", pid, offset)
		time.Sleep(3 * time.Second)
	}

}
