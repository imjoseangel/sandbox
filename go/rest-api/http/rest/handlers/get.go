package handlers

import (
	"errors"
	"net/http"
	"strconv"
	"time"

	"github.com/gorilla/mux"
	"github.com/imjoseangel/sandbox/go/rest-api/internal/todo/model"
	"github.com/imjoseangel/sandbox/go/rest-api/pkg/erru"
)

func (s service) Get() http.HandlerFunc {
	type response struct {
		ID          int          `json:"id"`
		Name        string       `json:"name"`
		Description string       `json:"description"`
		Status      model.Status `json:"status"`
		CreatedOn   time.Time    `json:"created_on"`
		UpdatedOn   *time.Time   `json:"updated_on,omitempty"`
	}
	return func(w http.ResponseWriter, r *http.Request) {
		vars := mux.Vars(r)

		id, err := strconv.Atoi(vars["id"])
		if err != nil {
			s.respond(w, erru.ErrArgument{
				Wrapped: errors.New("valid id must provide in path"),
			}, 0)
			return
		}

		getResponse, err := s.toDoService.Get(r.Context(), id)
		if err != nil {
			s.respond(w, err, 0)
			return
		}
		s.respond(w, response{
			ID:          getResponse.ID,
			Name:        getResponse.Name,
			Description: getResponse.Description,
			Status:      getResponse.Status,
			CreatedOn:   getResponse.CreatedOn,
			UpdatedOn:   getResponse.UpdatedOn,
		}, http.StatusOK)
	}
}
