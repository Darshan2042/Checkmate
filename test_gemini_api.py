"""
Test script to verify Google Gemini API is working correctly
"""

from dotenv import load_dotenv
import os
import google.generativeai as genai

def test_gemini_api():
    print("\n" + "="*80)
    print("GOOGLE GEMINI API TEST")
    print("="*80 + "\n")
    
    # Load environment variables
    load_dotenv(override=True)
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Test 1: Check if API key exists
    print("Test 1: Checking API Key...")
    if not api_key or api_key.strip() == "":
        print("  ✗ FAILED: GOOGLE_API_KEY not found in .env file")
        print("\n" + "="*80)
        return False
    else:
        print(f"  ✓ PASSED: API Key found (length: {len(api_key)} chars)")
        print(f"  Key preview: {api_key[:20]}...{api_key[-10:]}")
    
    # Test 2: Configure Gemini
    print("\nTest 2: Configuring Gemini API...")
    try:
        genai.configure(api_key=api_key.strip())
        print("  ✓ PASSED: API configured successfully")
    except Exception as e:
        print(f"  ✗ FAILED: {str(e)}")
        print("\n" + "="*80)
        return False
    
    # Test 3: List available models
    print("\nTest 3: Listing available models...")
    try:
        available_models = []
        for model_info in genai.list_models():
            if 'generateContent' in model_info.supported_generation_methods:
                available_models.append(model_info.name)
                print(f"  ✓ Found: {model_info.name}")
        
        if not available_models:
            print("  ⚠️  WARNING: No models with generateContent capability found")
        else:
            print(f"\n  ✓ PASSED: Found {len(available_models)} available model(s)")
    except Exception as e:
        print(f"  ⚠️  WARNING: Could not list models - {str(e)}")
        print("  (This is OK, will try fallback models)")
        available_models = []
    
    # Test 4: Initialize a model
    print("\nTest 4: Initializing a Gemini model...")
    model_names = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro", "gemini-1.0-pro"]
    
    if available_models:
        model_names = [available_models[0]] + model_names
    
    model = None
    for model_name in model_names:
        try:
            print(f"  Trying: {model_name}...")
            test_model = genai.GenerativeModel(model_name)
            print(f"    ✓ Initialized successfully")
            model = test_model
            break
        except Exception as e:
            print(f"    ✗ Failed: {str(e)}")
    
    if not model:
        print("\n  ✗ FAILED: Could not initialize any Gemini model")
        print("\n" + "="*80)
        return False
    else:
        print(f"\n  ✓ PASSED: Successfully initialized model")
    
    # Test 5: Simple text generation
    print("\nTest 5: Testing text generation...")
    try:
        response = model.generate_content("Say 'Hello, Gemini API is working!'")
        if response and hasattr(response, 'text'):
            print(f"  ✓ PASSED: Model responded")
            print(f"  Response: {response.text}")
        else:
            print(f"  ✗ FAILED: No text in response")
            return False
    except Exception as e:
        print(f"  ✗ FAILED: {str(e)}")
        
        # Check for specific error types
        error_msg = str(e)
        if "API_KEY" in error_msg.upper() or "INVALID" in error_msg.upper():
            print("\n  💡 HINT: Your API key appears to be invalid")
            print("     - Get a new key from: https://makersuite.google.com/app/apikey")
            print("     - Update .env file with: GOOGLE_API_KEY=your_new_key")
        elif "PERMISSION" in error_msg.upper() or "DENIED" in error_msg.upper():
            print("\n  💡 HINT: API not enabled for your account")
            print("     - Go to: https://console.cloud.google.com/")
            print("     - Enable 'Generative Language API'")
        elif "QUOTA" in error_msg.upper() or "EXCEEDED" in error_msg.upper():
            print("\n  💡 HINT: API quota exceeded")
            print("     - Wait a few minutes and try again")
            print("     - Check quota at: https://console.cloud.google.com/")
        
        print("\n" + "="*80)
        return False
    
    # All tests passed
    print("\n" + "="*80)
    print("✅ ALL TESTS PASSED!")
    print("="*80)
    print("\nYour Google Gemini API is configured correctly and ready to use.")
    print("You can now extract cheque data in the Streamlit app.\n")
    return True

if __name__ == "__main__":
    success = test_gemini_api()
    
    if not success:
        print("\n" + "="*80)
        print("TROUBLESHOOTING STEPS")
        print("="*80)
        print("\n1. Verify your API key:")
        print("   - Go to: https://makersuite.google.com/app/apikey")
        print("   - Create or copy your API key")
        print("   - Update .env file: GOOGLE_API_KEY=your_key_here")
        print("\n2. Enable the API:")
        print("   - Go to: https://console.cloud.google.com/")
        print("   - Search for 'Generative Language API'")
        print("   - Click 'Enable'")
        print("\n3. Check your quota:")
        print("   - Free tier: 60 requests per minute")
        print("   - View quota: https://console.cloud.google.com/iam-admin/quotas")
        print("\n" + "="*80 + "\n")
