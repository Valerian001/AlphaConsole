package main

import (
	"testing"
)

func TestNewAgentPool(t *testing.T) {
	size := 3
	pool := NewAgentPool(size)
	
	if pool.size != size {
		t.Errorf("Expected pool size %d, got %d", size, pool.size)
	}
}

func TestGetIdleShell(t *testing.T) {
	pool := NewAgentPool(1)
	// Mock a shell manually
	pool.shells = append(pool.shells, &AgentShell{ID: "test-1", Status: "IDLE"})
	
	shell := pool.GetIdleShell()
	if shell == nil {
		t.Fatal("Expected to get an idle shell, got nil")
	}
	
	if shell.Status != "BUSY" {
		t.Errorf("Expected shell status to be BUSY, got %s", shell.Status)
	}
	
	// Try to get another shell when none are idle
	shell2 := pool.GetIdleShell()
	if shell2 != nil {
		t.Error("Expected nil when no idle shells are available")
	}
}

func TestReleaseShell(t *testing.T) {
	pool := NewAgentPool(1)
	pool.shells = append(pool.shells, &AgentShell{ID: "test-1", Status: "BUSY"})
	
	pool.ReleaseShell("test-1")
	if pool.shells[0].Status != "IDLE" {
		t.Errorf("Expected shell status to be IDLE after release, got %s", pool.shells[0].Status)
	}
}
