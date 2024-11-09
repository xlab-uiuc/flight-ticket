****************************************************************
Prepared for Gabor's Data Analysis

Data Analysis for Business, Economics, and Policy
 by Gabor Bekes and  Gabor Kezdi
 Cambridge University Press 2021
 gabors-data-analysis.com 

Description of the 
airline-tickets-use dataset

used in case study 22A How does a merger between airlines affect prices?

Updated: 2023-02-13
****************************************************************
Data source

The data was collected and released by the
Bureau of Transportation Statistics (BTS) of the 
United States Department of Transportation (DOT)
DOT: https://www.transportation.gov
BTS: https://www.bts.gov

Airline Origin and Destination Survey (DB1B) 
https://www.
transtats.bts.gov/DatabaseInfo.asp?DB_ID=125
 " The Airline Origin and Destination Survey (DB1B) is a 10% sample of airline tickets from reporting carriers collected by the Office of Airline Information of the Bureau of Transportation Statistics. "

****************************************************************
Data access and copyright

The data is part of the United States Government Information System
You can use this publicly available data for educational purposes

Raw data (see below) is not stored in this repo. You may download it from the US BTS. You may also contact us to get access if there is a problem. https://gabors-data-analysis.com/contact-us/

****************************************************************
notes
y = year (for now 2011 and 2016 only)
q = quarter (1 to 4)
aiport code used here is the 3-letter string

****************************************************************
Raw data tables

DB1B_COUPONS_y_q.dta
 observations: itinerary level, n~3 million per quarter
 ID variable: itinid
 important variable(s): dest_id string for "destination:" all airports in the route except origin

Origin_and_Destination_Survey_DB1BTicket_y_q.csv
 observations: itinerary level, n ~ 3 million per quarter
 ID variable: itinid
 important variable(s): origin string for origin airport
		  dollarcred dollar credibility indicator
		  rpcarrier reporting carrier (airline)
		  passengers # passengers on itinerary (ticket)
		  itinfare airfare (total price of ticket)



****************************************************************
Tidy data tables

airline-route-panel.dta
 observations: 	airline X route X year X quarter level, 
			n ~ 600-700 th per quarter (total n=18,410,466)
 		  route: a unique combination of airports in itinerary (e.g., DTW MSP DTW)
		merged DB1B_COUPONS and DB!B_Ticket files, by itinid wihtin each quarter
			(ISSUE: some 20% of itineraries don't match; mostly only in DB1B_Ticket)
 ID variables:	airline (string) route (string) year quarter
		  (created from "origin" and "dest_id") 
 important variables: 
		passengers: total # passengers 
		itinfare: sum of airfare
		return:   whether return route 
			(calculated from route; if first 3 letters same as last 3 letters)
		return_sym:   whether symmretric return route 
 		finaldest: final destination, created from route
			   (non-return routes: last airport
			    return routes: middle airport, defined only for symmetric routes
			    missing value for 10% of passengers b/c non-symmetric return route)
		stops:  # stops (non-return routes: # airports between first and last airport
				return routes: only if symmetric route, # airport between first 
						and middle airport)

airline-originfinaldest-panel.dta
 observations: 	airline X origin X finaldest X return X year X quarter level, 
			n ~ 230 th per quarter total n=6,530,571)
		aggregated from airline-route-panel.dta (missing finaldest dropped)
 ID variables:	airline (string) origin (string) finaldest (string) return year quarter
 important variables: 
		passengers: total # passengers 
		itinfare: sum of airfare
		return_sym:   whether symmretric return route 
		stops:  # stops 


originfinaldest-panel.dta
 observations: 	origin X finaldest X return X year X quarter level, 
			n ~ 100th per quarter total n=2,670,174)
		aggregated from airline-route-panel.dta (missing finaldest dropped)
 ID variables:	origin (string) finaldest (string) return year quarter
 important variables: 
		passengers: total # passengers 
		average price: average of itinfare 
		return_sym:   whether symmretric return route 
		stops:  # stops 
		shareXX market share of each (XX) airline
		sharelargest: market share of largest airline



