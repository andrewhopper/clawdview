#!/usr/bin/env python3
try:
    from aws_bedrock_token_generator import provide_token
    
    def create_short_term_bedrock_key():
        print("Generating short-term Bedrock API key...")
        token = provide_token()
        
        print("\n=== SHORT-TERM BEDROCK API KEY ===")
        print(f"Bearer Token: {token}")
        print("Valid for: Up to 12 hours")
        print("==================================")
        
        return token
    
    if __name__ == "__main__":
        create_short_term_bedrock_key()
        
except ImportError:
    print("aws-bedrock-token-generator not installed")
    print("Install with: pip install aws-bedrock-token-generator")
    print("Then run this script again")
