package main

import (
	"fmt"
	"time"
)

func pinger(ping, pong chan string) {
	for data := range ping {
		notify(data)
		pong <- "pong"
	}
}
func ponger(ping, pong chan string) {
	for data := range pong {
		notify(data)
		ping <- "ping"
	}
}
func notify(msg string) {
	fmt.Println(msg)
	time.Sleep(time.Second)
}
func main() {
	fmt.Println("ping pong game")

	ping := make(chan string)
	pong := make(chan string)

	go pinger(ping, pong)
	go ponger(ping, pong)
	ping <- "ping"
	for {
	}
}
