package service

import (
	"github.com/imjoseangel/sandbox/go/rest-api/internal/todo/repository"
)

type Service struct {
	repo repository.Repository
}

func NewService(r repository.Repository) Service {
	return Service{
		repo: r,
	}
}
