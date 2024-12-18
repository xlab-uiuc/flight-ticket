#!/bin/bash
set -e

# Print environment variables for debugging
echo "WSK_API_HOST: $WSK_API_HOST"
echo "WSK_AUTH_KEY: $WSK_AUTH_KEY"

# Validate that required environment variables are set
if [ -z "$WSK_API_HOST" ] || [ -z "$WSK_AUTH_KEY" ]; then
  echo "Error: WSK_API_HOST and WSK_AUTH_KEY must be set."
  exit 1
fi

# Configure OpenWhisk CLI with the provided API host and auth key
echo "Configuring OpenWhisk CLI..."
wsk property set --apihost "$WSK_API_HOST" --auth "$WSK_AUTH_KEY"

# Run the main workload generator script
echo "Running the load generator..."
exec "$@"