#!/bin/bash
set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

: "${PYTHON_RUNTIME_IMAGE:?The deployer must declare the runtime used to build its action ZIPs}"

if [ -z "${WSK_API_HOST:-}" ] || [ -z "${WSK_AUTH_KEY:-}" ]; then
  echo "Error: WSK_API_HOST or WSK_AUTH_KEY not set."
  exit 1
fi

if [ -z "${REDIS_HOST:-}" ] || [ -z "${REDIS_PORT:-}" ]; then
  echo "Error. REDIS_HOST or REDIS_PORT not set."
  exit 1
fi

# Validate every build-time artifact before changing any registered actions.
for dir in actions/*; do
  unzip -tq "$dir/function.zip"
  unzip -p "$dir/function.zip" __main__.py >/dev/null
  unzip -p "$dir/function.zip" virtualenv/bin/activate_this.py >/dev/null
  unzip -p "$dir/function.zip" virtualenv/lib/python3.6/site-packages/redis/__init__.py >/dev/null
done

wsk property set --apihost "$WSK_API_HOST" --auth "$WSK_AUTH_KEY"

# Upsert only this application's actions, keeping unrelated catalog actions.
wsk -i action update query-for-travel actions/QueryForTravel/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param WSK_API_HOST "$WSK_API_HOST" \
  --param WSK_AUTH_KEY "$WSK_AUTH_KEY"
wsk -i action update seat-service actions/SeatService/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param WSK_API_HOST "$WSK_API_HOST" \
  --param WSK_AUTH_KEY "$WSK_AUTH_KEY"
wsk -i action update save-order-info actions/SaveOrderInfo/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action update query-for-station-id-by-station-name actions/QueryForStationIdByStationName/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action update query-config-entity-by-config-name actions/QueryConfigEntityByConfigName/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action update get-plane-type-by-trip-id actions/GetPlaneTypeByTripId/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action update get-plane-type-by-plane-type-id actions/GetPlaneTypeByPlaneTypeId/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param WSK_API_HOST "$WSK_API_HOST" \
  --param WSK_AUTH_KEY "$WSK_AUTH_KEY" \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action update get-sold-tickets actions/GetSoldTickets/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action update get-route-by-route-id actions/GetRouteByRouteId/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action update get-route-by-trip-id actions/GetRouteByTripId/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param WSK_API_HOST "$WSK_API_HOST" \
  --param WSK_AUTH_KEY "$WSK_AUTH_KEY" \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action update get-price-by-route-id-and-plane-type actions/GetPriceByRouteIdAndPlaneType/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action update get-order-by-id actions/GetOrderById/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action update drawback actions/Drawback/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action update cancel-service actions/CancelService/function.zip --docker "$PYTHON_RUNTIME_IMAGE" --timeout 120000 \
  --param WSK_API_HOST "$WSK_API_HOST" \
  --param WSK_AUTH_KEY "$WSK_AUTH_KEY"
