#!/bin/bash

if [ -z "$WSK_API_HOST" ] || [ -z "$WSK_AUTH_KEY" ]; then
  echo "Error: WSK_API_HOST or WSK_AUTH_KEY not set."
  exit 1
fi

if [ -z "$REDIS_HOST" ] || [ -z "$REDIS_PORT" ]; then
  echo "Error. REDIS_HOST or REDIS_PORT not set."
  exit 1
fi

wsk property set --apihost "$WSK_API_HOST" --auth "$WSK_AUTH_KEY"

for dir in actions/*; do
  (
    cd "$dir" || continue

    docker run --rm -v "$PWD:/tmp" openwhisk/python3action bash -c \
      "cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install redis"
    
    zip -r function.zip ./*
  )
done

wsk -i action create query-for-travel actions/QueryForTravel/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param WSK_API_HOST "$WSK_API_HOST" \
  --param WSK_AUTH_KEY "$WSK_AUTH_KEY"
wsk -i action create seat-service actions/SeatService/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param WSK_API_HOST "$WSK_API_HOST" \
  --param WSK_AUTH_KEY "$WSK_AUTH_KEY"
wsk -i action create save-order-info actions/SaveOrderInfo/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action create query-for-station-id-by-station-name actions/QueryForStationIdByStationName/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action create query-config-entity-by-config-name actions/QueryConfigEntityByConfigName/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action create get-plane-type-by-trip-id actions/GetPlaneTypeByTripId/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action create get-plane-type-by-plane-type-id actions/GetPlaneTypeByPlaneTypeId/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param WSK_API_HOST "$WSK_API_HOST" \
  --param WSK_AUTH_KEY "$WSK_AUTH_KEY"
wsk -i action create get-sold-tickets actions/GetSoldTickets/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param WSK_API_HOST "$WSK_API_HOST" \
  --param WSK_AUTH_KEY "$WSK_AUTH_KEY"
wsk -i action create get-route-by-route-id actions/GetRouteByRouteId/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action create get-route-by-trip-id actions/GetRouteByTripId/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param WSK_API_HOST "$WSK_API_HOST" \
  --param WSK_AUTH_KEY "$WSK_AUTH_KEY" \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action create get-price-by-route-id-and-plane-type actions/GetPriceByRouteIdAndPlaneType/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action create get-order-by-id actions/GetOrderById/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action create drawback actions/Drawback/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param REDIS_HOST "$REDIS_HOST" \
  --param REDIS_PORT "$REDIS_PORT"
wsk -i action create cancel-service actions/CancelService/function.zip --docker openwhisk/python3action --timeout 120000 \
  --param WSK_API_HOST "$WSK_API_HOST" \
  --param WSK_AUTH_KEY "$WSK_AUTH_KEY"