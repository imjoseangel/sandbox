package handlers

import (
	"github.com/gorilla/mux"
	toDoRepo "github.com/imjoseangel/sandbox/go/rest-api/internal/todo/repository"
	toDoService "github.com/imjoseangel/sandbox/go/rest-api/internal/todo/service"
	"github.com/jmoiron/sqlx"
	"github.com/sirupsen/logrus"
)

type service struct {
	logger      *logrus.Logger
	router      *mux.Router
	toDoService toDoService.Service
}

func newHandler(lg *logrus.Logger, db *sqlx.DB) service {
	return service{
		logger:      lg,
		toDoService: toDoService.NewService(toDoRepo.NewRepository(db)),
	}
}
