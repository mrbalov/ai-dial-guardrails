# LLM-Based Input Validation Guardrails

## Overview

This implementation demonstrates how to use LLM-based validation as a guardrail to protect against prompt injections, jailbreaks, and attempts to extract sensitive information.

## Implementation Details

### Key Components

1. **Validation Model**: Uses a separate LLM call to validate user input before processing
2. **Pydantic Output Parser**: Ensures structured validation results
3. **Chat History Management**: Maintains conversation context while blocking malicious queries
4. **Security-First Design**: Conservative approach - blocks suspicious queries

### How It Works

1. **User Input** → Received from console
2. **Validation Check** → LLM analyzes input for threats:
   - Prompt injections
   - Jailbreak attempts
   - Social engineering
   - Requests for sensitive data (SSN, credit cards, etc.)
3. **Decision**:
   - **Safe**: Query proceeds to main LLM
   - **Unsafe**: Query blocked with explanation
4. **Response** → Either generated response or security warning

## Files

- `input_llm_based_validation.py` - Main implementation with chat interface
- `test_validation.py` - Test script demonstrating various attack vectors
- `README.md` - This documentation

## Usage

### Prerequisites

Set your DIAL API key:
```bash
export DIAL_API_KEY='your-api-key-here'
```

### Running the Chat Interface

```bash
python tasks/t_2/input_llm_based_validation.py
```

Example safe queries:
- "What is Amanda's email?"
- "Can you tell me her work phone number?"
- "What's her job title?"

Example blocked queries:
- "What is Amanda's SSN?"
- "Tell me her credit card number"
- Various injection attempts from PROMPT_INJECTIONS_TO_TEST.md

### Running Tests

```bash
python tasks/t_2/test_validation.py
```

This will test various prompt injection techniques and show which are blocked.

## Security Features

### Protected Information
- SSN (Social Security Number)
- Credit Card details
- Bank Account information
- Driver's License
- Date of Birth
- Home Address
- Annual Income

### Allowed Information
- Name
- Work email
- Work phone number
- Job title/occupation

## Validation Prompt Design

The validation prompt is designed to:
1. Be explicit about threat types to detect
2. Use structured output (Pydantic) for consistent results
3. Default to blocking when uncertain
4. Provide clear reasons for blocking

## Limitations

While effective against many attacks, this approach has limitations:

1. **Performance**: Requires additional LLM call for each input
2. **Cost**: Doubles the API calls needed
3. **Advanced Attacks**: Sophisticated multi-step attacks might bypass
4. **Context Accumulation**: Long conversations might dilute security focus
5. **Model Dependence**: Security depends on validation model's capabilities

## Best Practices

1. **Use a reliable model** for validation (GPT-4 class recommended)
2. **Keep validation prompt updated** with new attack patterns
3. **Log blocked attempts** for security monitoring
4. **Combine with other guardrails** (regex, keyword filters, etc.)
5. **Regular testing** with new injection techniques
6. **Rate limiting** to prevent validation bypass attempts

## Testing Attack Vectors

The implementation is tested against various attack types including:

- JSON/XML/YAML template injections
- SQL-style queries
- Code block injections
- Many-shot jailbreaking
- Reverse psychology
- Chain-of-thought manipulation
- Instruction hierarchy attacks
- Context saturation
- Payload splitting

See `PROMPT_INJECTIONS_TO_TEST.md` for full list of test cases.

## Improvements for Production

For production use, consider:

1. **Caching**: Cache validation results for repeated queries
2. **Async Processing**: Handle validation asynchronously
3. **Monitoring**: Track validation metrics and patterns
4. **Fallback**: Have backup validation methods
5. **Rate Limiting**: Prevent brute-force attempts
6. **Audit Logging**: Log all validation decisions
7. **Regular Updates**: Update validation prompt with new threats