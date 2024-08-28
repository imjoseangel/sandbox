package main

import (
	"fmt"
	"syscall"

	seccomp "github.com/seccomp/libseccomp-golang"
)

func main() {
	// Set up a Seccomp filter and DENY ALL BY DEFAULT!
	defaultAction := seccomp.ActErrno.SetReturnCode(int16(syscall.EPERM))
	filter, err := seccomp.NewFilter(defaultAction)
	if err != nil {
		panic("Error creating Seccomp filter")
	}

	// Add allowed syscalls
	var syscalls = []string{
		"rt_sigaction", "mkdirat", "clone", "mmap", "readlinkat", "futex", "rt_sigprocmask",
		"mprotect", "write", "sigaltstack", "gettid", "read", "open", "close", "fstat",
		"munmap", "brk", "access", "execve", "getrlimit", "arch_prctl", "sched_getaffinity",
		"set_tid_address", "set_robust_list", "exit_group"}

	for _, call := range syscalls {
		syscallID, err := seccomp.GetSyscallFromName(call)
		if err != nil {
			panic(err)
		}
		// Here we allow the syscall in the list - one by one
		if err := filter.AddRule(syscallID, seccomp.ActAllow); err != nil {
			panic("Error adding rule for syscall")
		}
	}

	// Load the Seccomp filter
	if err := filter.Load(); err != nil {
		panic("Error loading Seccomp filter")
	}

	// Trigger our initial program
	err = syscall.Mkdir("/tmp/sec", 0755)
	if err != nil {
		panic(err)
	} else {
		fmt.Printf("Create a tmp file")
	}
}
