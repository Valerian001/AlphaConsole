package main

import (
	"fmt"
	"log"
	"os/exec"
	"sync"
)

type AgentShell struct {
	Process *exec.Cmd
	ID      string
	Status  string // IDLE, BUSY
}

type AgentPool struct {
	mu     sync.Mutex
	shells []*AgentShell
	size   int
}

func NewAgentPool(size int) *AgentPool {
	return &AgentPool{
		size:   size,
		shells: make([]*AgentShell, 0, size),
	}
}

func (p *AgentPool) Initialize() {
	p.mu.Lock()
	defer p.mu.Unlock()

	log.Printf("Initializing Warm Pool (Size: %d)...\n", p.size)
	for i := 0; i < p.size; i++ {
		shell := p.spawnShell(fmt.Sprintf("shell-%d", i))
		p.shells = append(p.shells, shell)
	}
}

func (p *AgentPool) spawnShell(id string) *AgentShell {
	// For now, we just spawn a placeholder python process
	// In production, this would be: python3 agents/core/base_shell.py
	cmd := exec.Command("python3", "-c", "import time; print('Shell Ready'); time.Sleep(3600)")
	
	err := cmd.Start()
	if err != nil {
		log.Printf("Failed to spawn shell %s: %v\n", id, err)
		return nil
	}

	log.Printf("Spawned Agent Shell: %s (PID: %d)\n", id, cmd.Process.Pid)
	return &AgentShell{
		Process: cmd,
		ID:      id,
		Status:  "IDLE",
	}
}

func (p *AgentPool) GetIdleShell() *AgentShell {
	p.mu.Lock()
	defer p.mu.Unlock()

	for _, s := range p.shells {
		if s.Status == "IDLE" {
			s.Status = "BUSY"
			return s
		}
	}
	return nil
}

func (p *AgentPool) ReleaseShell(id string) {
	p.mu.Lock()
	defer p.mu.Unlock()

	for _, s := range p.shells {
		if s.ID == id {
			s.Status = "IDLE"
			break
		}
	}
}
