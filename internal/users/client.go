package users

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"neurohunter/models"
	"strings"
	"time"
)

type Client struct {
	userFeaturesURL   string
	jobTitleGroupsURL string
	httpClient        *http.Client
}

func NewClient(
	userFeaturesURL, jobTitleGroupsURL string,
) (*Client, error) {
	endpoints := []struct {
		name string
		raw  string
	}{
		{name: "USER_FEATURES", raw: userFeaturesURL},
		{name: "JOB_TITLE_GROUPS", raw: jobTitleGroupsURL},
	}

	for _, endpoint := range endpoints {
		parsed, err := url.Parse(strings.TrimSpace(endpoint.raw))
		if err != nil {
			return nil, fmt.Errorf(
				"invalid %s URL: %w", endpoint.name, err,
			)
		}

		if parsed.Host == "" ||
			(parsed.Scheme != "http" && parsed.Scheme != "https") {
			return nil, fmt.Errorf(
				"%s must be an absolute HTTP(S) URL",
				endpoint.name,
			)
		}
	}

	return &Client{
		userFeaturesURL:   strings.TrimSpace(userFeaturesURL),
		jobTitleGroupsURL: strings.TrimSpace(jobTitleGroupsURL),
		httpClient: &http.Client{
			Timeout: 10 * time.Second,
		},
	}, nil
}

func (c *Client) GetUserFeatures(
	ctx context.Context,
) (map[string]models.UserFeature, error) {
	var features []models.UserFeature

	if err := c.getJSON(ctx, c.userFeaturesURL, &features); err != nil {
		return nil, fmt.Errorf("failed to fetch user features: %w", err)
	}

	featuresByID := make(map[string]models.UserFeature, len(features))

	for _, feature := range features {
		featuresByID[feature.UserID] = feature
	}

	return featuresByID, nil
}

func (c *Client) GetJobTitleGroups(
	ctx context.Context,
) (models.JobTitleGroups, error) {
	var groups models.JobTitleGroups

	if err := c.getJSON(ctx, c.jobTitleGroupsURL, &groups); err != nil {
		return nil, fmt.Errorf(
			"failed to fetch job title groups: %w",
			err,
		)
	}

	return groups, nil
}

func (c *Client) getJSON(
	ctx context.Context,
	url string,
	target any,
) error {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Accept", "application/json")

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("failed to perform request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode < http.StatusOK ||
		resp.StatusCode >= http.StatusMultipleChoices {
		body, _ := io.ReadAll(io.LimitReader(resp.Body, 4096))

		return fmt.Errorf(
			"Analyzer returned %s: %s",
			resp.Status,
			strings.TrimSpace(string(body)),
		)
	}

	if err := json.NewDecoder(resp.Body).Decode(target); err != nil {
		return fmt.Errorf("decode Analyzer response: %w", err)
	}

	return nil
}
