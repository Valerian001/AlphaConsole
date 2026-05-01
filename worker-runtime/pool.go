package main

import (
	"fmt"
	"log"
	"os/exec"
	"runtime"
	"sync"
)

type AgentShell struct {
	ID      string
	Status  string // IDLE, BUSY
	Current *exec.Cmd
}

type AgentPool struct {
	mu     sync.Mutex
	shells []*AgentShell
	size   int
}

func NewAgentPool() *AgentPool {
	size := CalculateOptimalSize()
	return &AgentPool{
		size:   size,
		shells: make([]*AgentShell, 0, size),
	}
}

func CalculateOptimalSize() int {
	cpus := runtime.NumCPU()
	if cpus > 8 { return 8 }
	if cpus < 2 { return 2 }
	return cpus
}

func (p *AgentPool) Initialize() {
	p.mu.Lock()
	defer p.mu.Unlock()

	log.Printf("Initializing Shell Slots (Optimal Size: %d)...\n", p.size)
	for i := 0; i < p.size; i++ {
		p.shells = append(p.shells, &AgentShell{
			ID:     fmt.Sprintf("shell-%d", i),
			Status: "IDLE",
		})
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
			s.Current = nil
			break
		}
	}
}

func (s *AgentShell) Run(script string, manifestPath string) error {
	s.Current = exec.Command("python3", script, manifestPath)
	return s.Current.Start()
}

func (s *AgentShell) Wait() error {
	if s.Current == nil {
		return fmt.Errorf("no process running")
	}
	return s.Current.Wait()
}
