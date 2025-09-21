#!/usr/bin/env bash

# Load variables from .env file located in project root (if exists)
ENV_FILE="$(dirname "$0")/../.env"
if [[ -f "$ENV_FILE" ]]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Verify required variables
: "${POSTGRES__USER:?Need POSTGRES__USER in .env}" 
: "${POSTGRES__PASSWORD:?Need POSTGRES__PASSWORD in .env}" 
: "${POSTGRES__HOSTS:?Need POSTGRES__HOSTS in .env}" 
: "${POSTGRES__PORT:?Need POSTGRES__PORT in .env}" 
: "${POSTGRES__DATABASE_NAME:?Need POSTGRES__DATABASE_NAME in .env}" 

# SSL and connection parameters
SSL_MODE="verify-full"
TARGET_SESSION_ATTRS="read-write"

# Build DSN with SSL parameters for master connection
DSN="postgresql://${POSTGRES__USER}:${POSTGRES__PASSWORD}@${POSTGRES__HOSTS}:${POSTGRES__PORT}/${POSTGRES__DATABASE_NAME}"
DSN="${DSN}?sslmode=${SSL_MODE}&target_session_attrs=${TARGET_SESSION_ATTRS}"

echo "Connecting to master database with SSL verification..."
echo "SSL Mode: ${SSL_MODE}"
echo "Target Session Attrs: ${TARGET_SESSION_ATTRS}"
echo ""
echo "Applying migrations in batch mode (non-interactive)..."

# Apply all unapplied migrations automatically without prompts
poetry run yoyo-migrate apply --batch -d "$DSN" migrations