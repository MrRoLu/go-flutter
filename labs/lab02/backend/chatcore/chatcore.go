package chatcore

import (
	"context"
	"sync"
)

// Message represents a chat message
// Sender, Recipient, Content, Broadcast, Timestamp
// TODO: Add more fields if needed

type Message struct {
	Sender    string
	Recipient string
	Content   string
	Broadcast bool
	Timestamp int64
}

// Broker handles message routing between users
// Contains context, input channel, user registry, mutex, done channel

type Broker struct {
	ctx        context.Context
	input      chan Message            // Incoming messages
	users      map[string]chan Message // userID -> receiving channel
	usersMutex sync.RWMutex            // Protects users map
	done       chan struct{}           // For shutdown
	// TODO: Add more fields if needed
}

// NewBroker creates a new message broker
func NewBroker(ctx context.Context) *Broker {
	// TODO: Initialize broker fields
	return &Broker{
		ctx:   ctx,
		input: make(chan Message, 100),
		users: make(map[string]chan Message),
		done:  make(chan struct{}),
	}
}

// Run starts the broker event loop (goroutine)
func (b *Broker) Run() {
	// TODO: Implement event loop (fan-in/fan-out pattern)
}

// SendMessage sends a message to the broker
func (b *Broker) SendMessage(msg Message) error {
	b.usersMutex.Lock()
	b.input <- msg
	b.usersMutex.Unlock()
	// TODO: Send message to appropriate channel/queue
	return nil
}

// RegisterUser adds a user to the broker
func (b *Broker) RegisterUser(userID string, recv chan Message) {
	b.usersMutex.RLock()
	_, exist := b.users[userID]
	b.usersMutex.RUnlock()

	b.usersMutex.Lock()
	defer b.usersMutex.Unlock()
	if exist {
		return
	} else {
		b.users[userID] = recv
	}
}

// TODO: Register user and their receiving channel

// UnregisterUser removes a user from the broker
func (b *Broker) UnregisterUser(userID string) {
	b.usersMutex.RLock()
	_, exists := b.users[userID]
	b.usersMutex.RUnlock()

	if exists {
		b.usersMutex.Lock()
		delete(b.users, userID)
		b.usersMutex.Unlock()
	} else {
		return
	}
	// TODO: Remove user from registry
}
