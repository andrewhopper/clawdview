#!/bin/zsh
mkdir -p ~/.aws

# Get andyhop credentials
eval $(/Users/andyhop/.toolbox/bin/isengardcli credentials andyhop@amazon.com)
ANDYHOP_KEY_ID=$AWS_ACCESS_KEY_ID
ANDYHOP_SECRET=$AWS_SECRET_ACCESS_KEY
ANDYHOP_TOKEN=$AWS_SESSION_TOKEN

# Get andyhop+bedrock credentials
eval $(/Users/andyhop/.toolbox/bin/isengardcli credentials andyhop+bedrock@amazon.com)
BEDROCK_KEY_ID=$AWS_ACCESS_KEY_ID
BEDROCK_SECRET=$AWS_SECRET_ACCESS_KEY
BEDROCK_TOKEN=$AWS_SESSION_TOKEN

# Write both profiles to credentials file
cat > ~/.aws/credentials << EOF
[default]
aws_access_key_id = $ANDYHOP_KEY_ID
aws_secret_access_key = $ANDYHOP_SECRET
aws_session_token = $ANDYHOP_TOKEN

[andyhop]
aws_access_key_id = $ANDYHOP_KEY_ID
aws_secret_access_key = $ANDYHOP_SECRET
aws_session_token = $ANDYHOP_TOKEN

[andyhopbedrock]
aws_access_key_id = $BEDROCK_KEY_ID
aws_secret_access_key = $BEDROCK_SECRET
aws_session_token = $BEDROCK_TOKEN
EOF
