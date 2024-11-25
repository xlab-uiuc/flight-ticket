#!/bin/bash
for dir in actions/*; do
    ( 
        cd "$dir" || continue
        docker run --rm -v "$PWD:/tmp" openwhisk/python3action bash -c \
        "cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
    )
done

wsk -i action create query-for-travel QueryForTravel/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create seat-service SeatService/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create save-order-info SaveOrderInfo/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create query-for-station-id-by-station-name QueryForStationIdByStationName/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create query-config-entity-by-config-name QueryConfigEntityByConfigName/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-airplane-type-by-trip-id GetAirplaneTypeByTripId/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-airplane-type-by-airplane-type-id GetAirplaneTypeByAirplaneTypeId/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-sold-tickets GetSoldTickets/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-route-by-route-id GetRouteByRouteId/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-route-by-trip-id GetRouteByTripId/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-price-by-route-id-and-airplane-type GetPriceByRouteIdAndAirplaneType/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-order-by-id GetOrderById/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create drawback Drawback/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create cancel-service CancelService/function.zip --docker openwhisk/python3action --timeout 120000

python3 populate_redis/add_distances.py
python3 populate_redis/add_entities.py
python3 populate_redis/add_money.py
python3 populate_redis/add_orders.py
python3 populate_redis/add_airplanes.py
python3 populate_redis/add_priceroute.py
python3 populate_redis/add_routes.py
python3 populate_redis/add_sId.py
python3 populate_redis/add_sold_tickets.py
python3 populate_redis/add_station.py
python3 populate_redis/add_trips.py
python3 populate_redis/reset_order_status.py
