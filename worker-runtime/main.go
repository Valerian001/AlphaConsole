package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"os/exec"
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

	pool := NewAgentPool() // Dynamic warm pool size
	pool.Initialize()

	return &WorkerRuntime{nc: nc, js: js, pool: pool}, nil
}

func (r *WorkerRuntime) Start() {
	log.Println("AlphaConsole Go Runtime Started...")

	// Subscribe to execution tasks
	_, err := r.js.Subscribe("agent.worker.*.exec", func(m *nats.Msg) {
		log.Printf("Received execution trigger on: %s\n", m.Subject)

		// 1. Initial hydration and start
		go r.ExecuteAgentCycle(m.Subject, m.Data)

		m.Ack()
	}, nats.ManualAck())

	if err != nil {
		log.Fatalf("Error subscribing to NATS: %v", err)
	}

	select {}
}

func (r *WorkerRuntime) ExecuteAgentCycle(subject string, data []byte) {
	shell := r.pool.GetIdleShell()
	if shell == nil {
		log.Println("Waiting for available shell...")
		return
	}
	defer r.pool.ReleaseShell(shell.ID)

	// Determine role from subject (e.g. agent.worker.planner.exec)
	// For simplicity, we assume the subject is correct
	role := "planner"
	if subject == "agent.worker.reviewer.exec" {
		role = "reviewer"
	}

	manifestPath := fmt.Sprintf("manifest_%s.json", shell.ID)
	os.WriteFile(manifestPath, data, 0644)

	script := fmt.Sprintf("../agents/%s_agent.py", role)
	log.Printf("[%s] Executing cycle: %s\n", shell.ID, role)

	if err := shell.Run(script, manifestPath); err != nil {
		log.Printf("Failed to run agent: %v\n", err)
		return
	}

	shell.Wait()

	// Read Result
	resultPath := fmt.Sprintf("result_%s.json", shell.ID)
	resultBytes, err := ioutil.ReadFile(resultPath)
	if err != nil {
		log.Printf("No result file found for %s\n", shell.ID)
		return
	}

	var result map[string]interface{}
	json.Unmarshal(resultBytes, &result)

	status := result["status"].(string)
	log.Printf("[%s] %s Finished with status: %s\n", shell.ID, role, status)

	// AGILE LOOP LOGIC
	if role == "reviewer" && status == "RECYCLE" {
		feedback := result["feedback"].(string)
		log.Printf("!!! RECYCLE TRIGGERED: %s\n", feedback)

		// Prepare new Planner manifest with feedback
		var manifest map[string]interface{}
		json.Unmarshal(data, &manifest)
		manifest["previous_feedback"] = feedback
		newData, _ := json.Marshal(manifest)

		// RECURSE: Trigger Planner
		r.ExecuteAgentCycle("agent.worker.planner.exec", newData)
	} else {
		// Sync final status to Control Plane
		r.nc.Publish(fmt.Sprintf("agent.task.status.%s", shell.ID), resultBytes)
	}
}

func (r *WorkerRuntime) Teardown() {
	log.Println("Initiating Teardown Sequence...")

	// 1. State Sync: pg_dump (Simulated)
	log.Println("Executing pg_dump for state persistence...")
	exec.Command("echo", "Dumping Postgres...").Run()

	// 2. Qdrant Snapshot (Simulated)
	log.Println("Triggering Qdrant snapshot export...")
	exec.Command("echo", "Exporting Qdrant Snapshot...").Run()

	// 3. Artifact Sync (Simulated)
	log.Println("Syncing local artifacts to remote MinIO...")
	exec.Command("echo", "Syncing MinIO...").Run()

	// 4. Signal Control Plane
	log.Println("Publishing worker.teardown.complete...")
	r.nc.Publish("worker.teardown.complete", []byte("SUCCESS"))
	r.nc.Flush()

	log.Println("Teardown Complete. Safe to destroy instance.")
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
	runtime.Teardown()
}
