"""
Basic Text Generation with Gemini API using Google GenAI SDK

This script demonstrates various text generation capabilities using the official
google-genai library.
"""

import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Initialize the client
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


def example_1_simple_generation():
    """Example 1: Simple text generation"""
    print("\n" + "="*60)
    print("Example 1: Simple Text Generation")
    print("="*60)
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='why is the sky blue?'
    )
    
    print(response.text)



def main():
    """Run all examples"""
    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return
    
    print("\n🚀 Gemini API Basic Text Generation Examples")
    print("Using Google GenAI SDK (google-genai)")
    
    try:
        # Run all examples
        example_1_simple_generation()

        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check that your GEMINI_API_KEY is valid")
        print("2. Ensure you have internet connectivity")
        print("3. Verify the API key has proper permissions")


if __name__ == "__main__":
    main()

