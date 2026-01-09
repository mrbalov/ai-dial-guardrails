#!/usr/bin/env python3
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import and run the main function
from tasks.t_3.output_llm_based_validation import main

# Run with soft_response=False by default
soft_mode = False
if len(sys.argv) > 1:
    soft_mode = sys.argv[1].lower() in ['true', 'soft', 'yes', '1']

print("Starting LLM-based PII validation guardrail...")
print(f"Soft response mode: {soft_mode}")
print("-" * 60)

try:
    main(soft_response=soft_mode)
except KeyboardInterrupt:
    print("\n\nExiting...")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()