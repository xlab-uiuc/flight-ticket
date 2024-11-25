#!/bin/bash
for dir in actions/*; do
    ( 
        cd "$dir" || continue
        docker run --rm -v "$PWD:/tmp" openwhisk/python3action bash -c \
        "cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
    )
done

wsk -i action create query-for-travel action/QueryForTravel/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create seat-service action/SeatService/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create save-order-info action/SaveOrderInfo/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create query-for-station-id-by-station-name action/QueryForStationIdByStationName/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create query-config-entity-by-config-name action/QueryConfigEntityByConfigName/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-plane-type-by-trip-id action/GetPlaneTypeByTripId/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-plane-type-by-plane-type-id action/GetPlaneTypeByPlaneTypeId/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-sold-tickets action/GetSoldTickets/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-route-by-route-id action/GetRouteByRouteId/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-route-by-trip-id action/GetRouteByTripId/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-price-by-route-id-and-plane-type action/GetPriceByRouteIdAndPlaneType/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-order-by-id action/GetOrderById/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create drawback action/Drawback/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create cancel-service action/CancelService/function.zip --docker openwhisk/python3action --timeout 120000

python3 populate_redis/add_distances.py
python3 populate_redis/add_entities.py
python3 populate_redis/add_money.py
python3 populate_redis/add_orders.py
python3 populate_redis/add_planes.py
python3 populate_redis/add_priceroute.py
python3 populate_redis/add_sId.py
python3 populate_redis/add_sold_tickets.py
python3 populate_redis/add_station.py
python3 populate_redis/add_trips.py
# python3 populate_redis/reset_order_status.py
