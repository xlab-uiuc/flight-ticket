#   !/bin/bash
for dir in actions/*; do
    ( 
        cd "$dir" || continue
        docker run --rm -v "$PWD:/tmp" openwhisk/python3action bash -c \
        "cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
        zip -r function.zip ./*
    )
done

wsk -i action create query-for-travel actions/QueryForTravel/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create seat-service actions/SeatService/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create save-order-info actions/SaveOrderInfo/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create query-for-station-id-by-station-name actions/QueryForStationIdByStationName/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create query-config-entity-by-config-name actions/QueryConfigEntityByConfigName/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-plane-type-by-trip-id actions/GetPlaneTypeByTripId/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-plane-type-by-plane-type-id actions/GetPlaneTypeByPlaneTypeId/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-sold-tickets actions/GetSoldTickets/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-route-by-route-id actions/GetRouteByRouteId/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-route-by-trip-id actions/GetRouteByTripId/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-price-by-route-id-and-plane-type actions/GetPriceByRouteIdAndPlaneType/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create get-order-by-id actions/GetOrderById/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create drawback actions/Drawback/function.zip --docker openwhisk/python3action --timeout 120000
wsk -i action create cancel-service actions/CancelService/function.zip --docker openwhisk/python3action --timeout 120000

python3 populate_redis/add_distances.py
python3 populate_redis/add_station.py
python3 populate_redis/add_money.py
python3 populate_redis/add_orders.py
python3 populate_redis/add_trips.py
python3 populate_redis/add_planes.py
python3 populate_redis/add_priceroute.py
python3 populate_redis/add_sId.py
python3 populate_redis/add_sold_tickets.py
python3 populate_redis/add_entities.py
# python3 populate_redis/reset_order_status.py
