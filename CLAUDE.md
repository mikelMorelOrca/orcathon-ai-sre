# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project called "revamp" that implements an SRE monitoring agent using the Agno framework. The agent analyzes Slack channels to identify and summarize infrastructure incidents and issues.

## Development Commands

### Environment Setup
```bash
# Use uv for package management (uv.lock present)
uv sync                    # Install dependencies
uv run python main.py      # Run the main application
```

### Environment Variables
The project requires these environment variables in `.env`:
- `AWS_PROFILE` - AWS profile for Bedrock access
- `AWS_REGION` - AWS region
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `MODEL` - AWS Bedrock model ID
- `SLACK_BOT_TOKEN` - Slack bot token for API access

## Architecture

### Core Components

- **main.py**: Entry point that configures and runs the SRE monitoring agent
- **slack_tools.py**: Comprehensive Slack API integration providing tools for:
  - Channel and message retrieval
  - Thread conversation analysis
  - User and channel information lookup
  - Message filtering and data extraction

### Agent Configuration
The system uses Agno framework with:
- AWS Bedrock for LLM backend
- DuckDuckGo search tools
- Custom Slack tools for incident monitoring
- Configured as an SRE engineer with debug mode enabled

### Slack Tools Architecture
The slack_tools.py module provides a complete Slack API wrapper with:
- `SlackClient` class for authenticated API calls
- Multiple `@tool` decorated functions for agent integration
- Built-in caching for users, channels, and subteams
- Error handling and rate limiting

## Key Dependencies

- `agno>=1.8.1` - AI agent framework
- `boto3>=1.40.25` - AWS SDK for Bedrock integration
- `requests>=2.32.5` - HTTP client for Slack API
- `ddgs>=9.5.5`, `duckduckgo-search>=8.1.1` - Search capabilities