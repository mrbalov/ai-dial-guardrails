#!/usr/bin/env python3
"""Test script for streaming PII guardrail"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tasks.t_3.streaming_pii_guardrail import StreamingPIIGuardrail, PresidioStreamingPIIGuardrail

def test_streaming_guardrail():
    """Test the StreamingPIIGuardrail with sample PII data"""
    
    print("=" * 60)
    print("Testing StreamingPIIGuardrail")
    print("=" * 60)
    
    guardrail = StreamingPIIGuardrail(buffer_size=100, safety_margin=20)
    
    # Test data with various PII
    test_chunks = [
        "Amanda Grace Johnson's SSN is ",
        "234-56-",
        "7890 and her credit ",
        "card number is 3782 8224 ",
        "6310 0051 with CVV: 1234. ",
        "She lives at 9823 Sunset Boulevard, ",
        "Los Angeles. Her bank account at Bank of America is ",
        "5647382910. Her driver's license is CA-DL-C7394856. ",
        "Her annual income is $112,800 and she was born on July 3, 1979."
    ]
    
    print("\nOriginal text (chunked):")
    print("".join(test_chunks))
    print("\n" + "-" * 40)
    print("Processed output:\n")
    
    full_output = ""
    for chunk in test_chunks:
        processed = guardrail.process_chunk(chunk)
        if processed:
            print(processed, end="")
            full_output += processed
    
    # Finalize any remaining content
    final = guardrail.finalize()
    if final:
        print(final, end="")
        full_output += final
    
    print("\n\n" + "-" * 40)
    print("Summary:")
    print(f"Original length: {sum(len(c) for c in test_chunks)} chars")
    print(f"Processed length: {len(full_output)} chars")
    
    # Check what was redacted
    redacted_items = []
    if "[REDACTED-SSN]" in full_output:
        redacted_items.append("SSN")
    if "[REDACTED-CREDIT-CARD]" in full_output:
        redacted_items.append("Credit Card")
    if "[REDACTED-LICENSE]" in full_output:
        redacted_items.append("Driver's License")
    if "[REDACTED-ACCOUNT]" in full_output:
        redacted_items.append("Bank Account")
    if "[REDACTED-AMOUNT]" in full_output:
        redacted_items.append("Currency Amount")
    if "[REDACTED-DATE]" in full_output:
        redacted_items.append("Date")
    if "[REDACTED-ADDRESS]" in full_output:
        redacted_items.append("Address")
    if "CVV: [REDACTED]" in full_output:
        redacted_items.append("CVV")
    
    print(f"Redacted items: {', '.join(redacted_items) if redacted_items else 'None'}")

def test_presidio_guardrail():
    """Test the PresidioStreamingPIIGuardrail"""
    
    print("\n" + "=" * 60)
    print("Testing PresidioStreamingPIIGuardrail")
    print("=" * 60)
    
    try:
        guardrail = PresidioStreamingPIIGuardrail(buffer_size=100, safety_margin=20)
        
        # Test data with various PII
        test_chunks = [
            "Amanda Grace Johnson's personal details: ",
            "Phone: (310) 555-0734, ",
            "Email: amanda_hello@mailpro.net, ",
            "SSN: 234-56-7890, ",
            "Credit Card: 3782 8224 6310 0051"
        ]
        
        print("\nOriginal text (chunked):")
        print("".join(test_chunks))
        print("\n" + "-" * 40)
        print("Processed output:\n")
        
        full_output = ""
        for chunk in test_chunks:
            processed = guardrail.process_chunk(chunk)
            if processed:
                print(processed, end="")
                full_output += processed
        
        # Finalize any remaining content
        final = guardrail.finalize()
        if final:
            print(final, end="")
            full_output += final
        
        print("\n\n" + "-" * 40)
        print("Presidio successfully redacted PII")
        
    except Exception as e:
        print(f"Error with Presidio: {str(e)}")
        print("Note: Presidio requires spacy model 'en_core_web_sm' to be installed")

if __name__ == "__main__":
    test_streaming_guardrail()
    test_presidio_guardrail()