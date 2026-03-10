#!/usr/bin/env python3
import boto3
import json

def create_long_term_bedrock_key():
    username = "bedrock-api-user"
    expiration_days = 30
    
    iam_client = boto3.client("iam")
    
    try:
        # Create IAM user
        print("Creating IAM user...")
        user_response = iam_client.create_user(UserName=username)
        print(f"Created user: {username}")
        
        # Attach Bedrock policy
        print("Attaching Bedrock policy...")
        policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockLimitedAccess"
        iam_client.attach_user_policy(
            UserName=username,
            PolicyArn=policy_arn
        )
        print("Policy attached successfully")
        
        # Create service-specific credential (API key)
        print("Generating API key...")
        credential_response = iam_client.create_service_specific_credential(
            UserName=username,
            ServiceName="bedrock.amazonaws.com"
        )
        
        api_key = credential_response["ServiceSpecificCredential"]["ServiceSpecificCredentialId"]
        secret_key = credential_response["ServiceSpecificCredential"]["ServicePassword"]
        
        print("\n=== BEDROCK API KEY GENERATED ===")
        print(f"API Key ID: {api_key}")
        print(f"Secret Key: {secret_key}")
        print(f"User: {username}")
        print("=================================")
        
        return {
            "api_key": api_key,
            "secret_key": secret_key,
            "username": username
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    create_long_term_bedrock_key()
