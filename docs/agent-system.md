# Agent System

## Implemented Agents

### Style Analysis Agent
- **Input:** Sample texts
- **Output:** Persona JSON
- **Engine:** LLM-powered
- **Purpose:** Analyze creator's writing style and generate persona

### Strategy Agent
- **Input:** Persona + Preferences
- **Output:** Weekly content plan
- **Purpose:** Generate weekly content strategy based on creator's persona

### Script Agent
- **Input:** Persona + Preferences + Topic
- **Output:** Reel script
- **Purpose:** Generate individual reel scripts that match creator's style

## Agent Requirements

All agents must follow these requirements:

### Technical Requirements
- **Stateless:** No internal state between calls
- **JSON-in / JSON-out:** Clean data contracts
- **No DB or HTTP logic:** Pure business logic only
- **Replaceable implementations:** LLM provider agnostic

### Input/Output Contracts
- All inputs must be validated before processing
- All outputs must be valid JSON matching defined schemas
- Error handling must return structured error responses

### Integration Rules
- Agents are called by service layer only
- No direct database access
- No HTTP request handling
- No authentication logic

## Agent Development Guidelines

When creating new agents:

1. Define clear input/output schemas
2. Implement validation for all inputs
3. Keep business logic pure and testable
4. Make LLM calls replaceable
5. Follow existing agent patterns