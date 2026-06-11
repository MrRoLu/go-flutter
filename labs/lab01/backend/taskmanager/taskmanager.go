package taskmanager

import (
	"errors"
	"time"
)

// Predefined errors
var (
	ErrTaskNotFound = errors.New("task not found")
	ErrEmptyTitle   = errors.New("title cannot be empty")
)

// Task represents a single task
type Task struct {
	ID          int
	Title       string
	Description string
	Done        bool
	CreatedAt   time.Time
}

// TaskManager manages a collection of tasks
type TaskManager struct {
	tasks  map[int]Task
	nextID int
}

// NewTaskManager creates a new task manager
func NewTaskManager() *TaskManager {
	return &TaskManager{
		tasks:  make(map[int]Task),
		nextID: 1,
	}
}

// AddTask adds a new task to the manager, returns an error if the title is empty, and increments the nextID
func (tm *TaskManager) AddTask(title, description string) (Task, error) {
	if title == "" {
		return Task{ID: tm.nextID}, ErrEmptyTitle
	}

	newNextID := tm.nextID

	tm.tasks[newNextID] = Task{
		ID:          newNextID,
		Title:       title,
		Description: description,
		Done:        false,
		CreatedAt:   time.Now(),
	}

	tm.nextID++

	return tm.tasks[newNextID], nil
}

// UpdateTask updates an existing task, returns an error if the title is empty or the task is not found
func (tm *TaskManager) UpdateTask(id int, title, description string, done bool) error {
	if title == "" {
		return ErrEmptyTitle
	}

	if _, exists := tm.tasks[id]; exists {
		tm.tasks[id] = Task{
			Title:       title,
			Description: description,
			Done:        done,
		}

		return nil
	} else {
		return ErrTaskNotFound
	}
}

// DeleteTask removes a task from the manager, returns an error if the task is not found
func (tm *TaskManager) DeleteTask(id int) error {
	if _, exists := tm.tasks[id]; exists {
		delete(tm.tasks, id)

		return nil
	} else {
		return ErrTaskNotFound
	}
}

// GetTask retrieves a task by ID, returns an error if the task is not found
func (tm *TaskManager) GetTask(id int) (Task, error) {
	if _, exists := tm.tasks[id]; exists {
		return tm.tasks[id], nil
	} else {
		return Task{}, ErrTaskNotFound
	}
}

// ListTasks returns all tasks, optionally filtered by done status, returns an empty slice if no tasks are found
func (tm *TaskManager) ListTasks(filterDone *bool) []Task {
	var listTasks []Task

	if tm == nil || tm.tasks == nil {
		return []Task{}
	}

	listTasks = make([]Task, 0, len(tm.tasks))

	for _, v := range tm.tasks {
		if filterDone == nil || v.Done == *filterDone {
			listTasks = append(listTasks, v)
		}
	}

	return listTasks
}
