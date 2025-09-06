package genai

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"strings"

	"github.com/openai/openai-go"
	"mckinsey.com/ark/internal/common"
	"sigs.k8s.io/controller-runtime/pkg/client"
	logf "sigs.k8s.io/controller-runtime/pkg/log"
)

type HTTPMemory struct {
	client     client.Client
	httpClient *http.Client
	baseURL    string
	sessionId  string
	name       string
	namespace  string
	recorder   EventEmitter
}

func NewHTTPMemory(ctx context.Context, k8sClient client.Client, memoryName, namespace string, recorder EventEmitter, config Config) (MemoryInterface, error) {
	if k8sClient == nil || memoryName == "" || namespace == "" {
		return nil, fmt.Errorf("invalid parameters")
	}

	memory, err := getMemoryResource(ctx, k8sClient, memoryName, namespace)
	if err != nil {
		return nil, err
	}

	// Use the lastResolvedAddress as our initial baseline
	if memory.Status.LastResolvedAddress == nil || *memory.Status.LastResolvedAddress == "" {
		return nil, fmt.Errorf("memory has no lastResolvedAddress in status")
	}

	sessionId := config.SessionId
	if sessionId == "" {
		sessionId = string(memory.UID)
	}

	httpClient := common.NewHTTPClientWithLogging(ctx)
	if config.Timeout > 0 {
		httpClient.Timeout = config.Timeout
	}

	return &HTTPMemory{
		client:     k8sClient,
		httpClient: httpClient,
		baseURL:    strings.TrimSuffix(*memory.Status.LastResolvedAddress, "/"),
		sessionId:  sessionId,
		name:       memoryName,
		namespace:  namespace,
		recorder:   recorder,
	}, nil
}

// resolveAndUpdateAddress dynamically resolves the memory address and updates the status if it changed
func (m *HTTPMemory) resolveAndUpdateAddress(ctx context.Context) error {
	memory, err := getMemoryResource(ctx, m.client, m.name, m.namespace)
	if err != nil {
		return fmt.Errorf("failed to get memory resource: %w", err)
	}

	// Resolve the address using ValueSourceResolver
	resolver := common.NewValueSourceResolver(m.client)
	resolvedAddress, err := resolver.ResolveValueSource(ctx, memory.Spec.Address, m.namespace)
	if err != nil {
		return fmt.Errorf("failed to resolve memory address: %w", err)
	}

	// Check if address changed from current baseURL
	newBaseURL := strings.TrimSuffix(resolvedAddress, "/")
	if m.baseURL != newBaseURL {
		// Update the Memory status with new address
		memory.Status.LastResolvedAddress = &resolvedAddress
		memory.Status.Message = fmt.Sprintf("Address dynamically resolved to: %s", resolvedAddress)

		// Update the status in Kubernetes
		if err := m.client.Status().Update(ctx, memory); err != nil {
			// Log error but don't fail the request
			logCtx := logf.FromContext(ctx)
			logCtx.Error(err, "failed to update Memory status with new address",
				"memory", m.name, "namespace", m.namespace, "newAddress", resolvedAddress)
		}
	}

	// Update the baseURL
	m.baseURL = strings.TrimSuffix(resolvedAddress, "/")
	return nil
}

func (m *HTTPMemory) AddMessages(ctx context.Context, messages []Message) error {
	if len(messages) == 0 {
		return nil
	}

	// Resolve address dynamically
	if err := m.resolveAndUpdateAddress(ctx); err != nil {
		return err
	}

	tracker := NewOperationTracker(m.recorder, ctx, "MemoryAddMessages", m.name, map[string]string{
		"namespace": m.namespace,
		"sessionId": m.sessionId,
		"messages":  fmt.Sprintf("%d", len(messages)),
	})

	// Convert messages to the request format
	openaiMessages := make([]openai.ChatCompletionMessageParamUnion, len(messages))
	for i, msg := range messages {
		openaiMessages[i] = openai.ChatCompletionMessageParamUnion(msg)
	}

	reqBody, err := json.Marshal(MessagesRequest{Messages: openaiMessages})
	if err != nil {
		tracker.Fail(fmt.Errorf("failed to serialize messages: %w", err))
		return fmt.Errorf("failed to serialize messages: %w", err)
	}

	requestURL := fmt.Sprintf("%s%s/%s", m.baseURL, MessagesEndpoint, url.QueryEscape(m.sessionId))
	req, err := http.NewRequestWithContext(ctx, http.MethodPut, requestURL, bytes.NewReader(reqBody))
	if err != nil {
		tracker.Fail(fmt.Errorf("failed to create request: %w", err))
		return fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Content-Type", ContentTypeJSON)
	req.Header.Set("User-Agent", UserAgent)

	resp, err := m.httpClient.Do(req)
	if err != nil {
		tracker.Fail(fmt.Errorf("HTTP request failed: %w", err))
		return fmt.Errorf("HTTP request failed: %w", err)
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		err := fmt.Errorf("HTTP status %d", resp.StatusCode)
		tracker.Fail(err)
		return err
	}

	tracker.Complete("messages added")
	return nil
}

func (m *HTTPMemory) GetMessages(ctx context.Context) ([]Message, error) {
	// Resolve address dynamically
	if err := m.resolveAndUpdateAddress(ctx); err != nil {
		return nil, err
	}

	tracker := NewOperationTracker(m.recorder, ctx, "MemoryGetMessages", m.name, map[string]string{
		"namespace": m.namespace,
		"sessionId": m.sessionId,
	})

	requestURL := fmt.Sprintf("%s%s/%s", m.baseURL, MessagesEndpoint, url.QueryEscape(m.sessionId))
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, requestURL, nil)
	if err != nil {
		tracker.Fail(fmt.Errorf("failed to create request: %w", err))
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Accept", ContentTypeJSON)
	req.Header.Set("User-Agent", UserAgent)

	resp, err := m.httpClient.Do(req)
	if err != nil {
		tracker.Fail(fmt.Errorf("HTTP request failed: %w", err))
		return nil, fmt.Errorf("HTTP request failed: %w", err)
	}
	defer func() { _ = resp.Body.Close() }()

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		err := fmt.Errorf("HTTP status %d", resp.StatusCode)
		tracker.Fail(err)
		return nil, err
	}

	var response MessagesResponse
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		tracker.Fail(fmt.Errorf("failed to decode response: %w", err))
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	messages := make([]Message, 0, len(response.Messages))
	for i, rawMsg := range response.Messages {
		var openaiMessage openai.ChatCompletionMessageParamUnion
		if err := json.Unmarshal(rawMsg, &openaiMessage); err != nil {
			err := fmt.Errorf("failed to unmarshal message at index %d: %w", i, err)
			tracker.Fail(err)
			return nil, err
		}
		messages = append(messages, Message(openaiMessage))
	}

	// Update metadata with message count
	tracker.metadata["messages"] = fmt.Sprintf("%d", len(messages))
	tracker.Complete("retrieved")
	return messages, nil
}

func (m *HTTPMemory) Close() error {
	if m.httpClient != nil {
		m.httpClient.CloseIdleConnections()
	}
	return nil
}
