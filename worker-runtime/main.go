package main

import (
	"log"
	"os"
	"os/signal"
	"syscall"

	"github.com/nats-io/nats.go"
)

type WorkerRuntime struct {
	nc   *nats.Conn
	js   nats.JetStreamContext
	pool *AgentPool
}

func NewWorkerRuntime(natsURL string) (*WorkerRuntime, error) {
	nc, err := nats.Connect(natsURL)
	if err != nil {
		return nil, err
	}

	js, err := nc.JetStream()
	if err != nil {
		return nil, err
	}

	pool := NewAgentPool(5) // Default warm pool size
	pool.Initialize()

	return &WorkerRuntime{nc: nc, js: js, pool: pool}, nil
}

func (r *WorkerRuntime) Start() {
	log.Println("AlphaConsole Go Runtime Started...")

	// Subscribe to assigned tasks for this worker
	// Subject: task.*.assigned
	_, err := r.js.Subscribe("task.*.assigned", func(m *nats.Msg) {
		log.Printf("Received task on subject: %s\n", m.Subject)

		// Select Idle Shell from Warm Pool
		shell := r.pool.GetIdleShell()
		if shell == nil {
			log.Println("No idle shells available, task queued or dropped.")
			return
		}

		log.Printf("Hydrating shell %s for task...\n", shell.ID)

		// 3. Hydrate Shell (Write manifest, signal process)
		// 4. Execute

		m.Ack()
	}, nats.ManualAck())

	if err != nil {
		log.Fatalf("Error subscribing to NATS: %v", err)
	}

	// Keep alive
	select {}
}

func main() {
	natsURL := os.Getenv("NATS_URL")
	if natsURL == "" {
		natsURL = nats.DefaultURL
	}

	runtime, err := NewWorkerRuntime(natsURL)
	if err != nil {
		log.Fatalf("Failed to initialize runtime: %v", err)
	}

	go runtime.Start()

	// Wait for exit
	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
	<-sig
	log.Println("Shutting down AlphaConsole Go Runtime...")
}
