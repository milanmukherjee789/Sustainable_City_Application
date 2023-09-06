# Dublin Transit API (Node.js & Hapi)
This is an API designed for real-time transit information for Dublin Bus and Luas services, implemented in Node.js using the Hapi framework. The API gathers data from the official real-time sources of both Dublin Bus and Luas, and then converts it into a user-friendly JSON format for easy consumption by clients.

endpoints:

```
GET /bus/routes
GET /bus/route/{route_number}
GET /bus/stop/{stop_number}

GET /luas/stops
GET /luas/stop/{stop_id}
```

### Requires

* nodejs v8 +

### To run

```
npm install
npm start
```
## Sample Responses
* GET: http://localhost:8000/luas/stop/{Stop_ID}
(Stop ID example : MUS,RAN)

```
{
	"created": "2023-03-27T20:00:50",
	"stop": "Museum",
	"stopAbv": "MUS",
	"message": "Red Line services operating normally",
	"direction": [
		{
			"name": "Inbound",
			"tram": [
				{
					"dueMins": "1",
					"destination": "The Point"
				},
				{
					"dueMins": "10",
					"destination": "The Point"
				}
			]
		},
		{
			"name": "Outbound",
			"tram": [
				{
					"dueMins": "6",
					"destination": "Tallaght"
				},
				{
					"dueMins": "17",
					"destination": "Tallaght"
				}
			]
		}
	]
}
```

* GET: http://localhost:8000/bus/route/{Bus_Number}
(Bus Number eg 26,115 etc )
```
{
	"route": "26",
	"stops": {
		"Route": {
			"attributes": {
				"diffgr:id": "Route1",
				"msdata:rowOrder": "0"
			},
			"RouteID": "2155",
			"RouteNumber": "26",
			"RouteDescription": "From Merrion Sq. Towards Liffey Valley",
			"StartStageID": "910",
			"EndStageID": "790",
			"DepotID": "4",
			"IsDisabled": "true",
			"IsExpresso": "false",
			"IsNitelink": "false",
			"IsAirlink": "false",
			"IsRaillink": "false",
			"IsSchoollink": "false",
			"InBoundFrequency": "4",
			"OutBoundFrequency": "4",
			"InBoundPattern": "261005",
			"OutBoundPattern": "260003",
			"RouteCategoryID": "1",
			"IsMinimumFare": "false",
			"StartStageName": "Merrion Sq.",
			"EndStageName": "Liffey Valley Shopping Centre"
		},
		"InboundStop": [
			{
				"attributes": {
					"diffgr:id": "InboundStop1",
					"msdata:rowOrder": "0"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "7884",
				"Address": "Liffey Valley",
				"Location": "Plaza",
				"SeqNumber": "5",
				"Latitude": "53.354099",
				"Longitude": "-6.392018",
				"SeqNumberExt": "5"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop2",
					"msdata:rowOrder": "1"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "4715",
				"Address": "Liffey Valley SC",
				"Location": "Fonthill Road",
				"SeqNumber": "10",
				"Latitude": "53.352719",
				"Longitude": "-6.395725",
				"SeqNumberExt": "10"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop3",
					"msdata:rowOrder": "2"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2686",
				"Address": "Sports Club",
				"Location": "Coldcut Rd",
				"SeqNumber": "20",
				"Latitude": "53.347583",
				"Longitude": "-6.388689",
				"SeqNumberExt": "20"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop4",
					"msdata:rowOrder": "3"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "7510",
				"Address": "Cloverhill Road",
				"Location": "Coldcut Rd",
				"SeqNumber": "25",
				"Latitude": "53.347196",
				"Longitude": "-6.384513",
				"SeqNumberExt": "25"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop5",
					"msdata:rowOrder": "4"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2207",
				"Address": "Kennelsfort Road",
				"Location": "Palmerstown Road",
				"SeqNumber": "30",
				"Latitude": "53.346757",
				"Longitude": "-6.379637",
				"SeqNumberExt": "30"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop6",
					"msdata:rowOrder": "5"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2208",
				"Address": "Kennelsfort Green",
				"Location": "Kennelsfort Road",
				"SeqNumber": "35",
				"Latitude": "53.34991",
				"Longitude": "-6.37777",
				"SeqNumberExt": "35"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop7",
					"msdata:rowOrder": "6"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2210",
				"Address": "Woodfarm",
				"Location": "Palmerstown Cemetery",
				"SeqNumber": "40",
				"Latitude": "53.352422",
				"Longitude": "-6.378287",
				"SeqNumberExt": "40"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop8",
					"msdata:rowOrder": "7"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2211",
				"Address": "Palmerstown Avenue",
				"Location": "Kennelsfort Rd",
				"SeqNumber": "45",
				"Latitude": "53.353957",
				"Longitude": "-6.374567",
				"SeqNumberExt": "45"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop9",
					"msdata:rowOrder": "8"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2241",
				"Address": "Kennelsfort Road",
				"Location": "Lucan Road",
				"SeqNumber": "45",
				"Latitude": "53.354924",
				"Longitude": "-6.371259",
				"SeqNumberExt": "45"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop10",
					"msdata:rowOrder": "9"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2242",
				"Address": "The Oval",
				"Location": "Lucan Road",
				"SeqNumber": "50",
				"Latitude": "53.353924",
				"Longitude": "-6.366989",
				"SeqNumberExt": "50"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop11",
					"msdata:rowOrder": "10"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2243",
				"Address": "Glenaulin",
				"Location": "Lucan Road",
				"SeqNumber": "55",
				"Latitude": "53.351967",
				"Longitude": "-6.355685",
				"SeqNumberExt": "55"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop12",
					"msdata:rowOrder": "11"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2244",
				"Address": "Belgrove Park",
				"Location": "Lucan Road",
				"SeqNumber": "60",
				"Latitude": "53.35088",
				"Longitude": "-6.351592",
				"SeqNumberExt": "60"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop13",
					"msdata:rowOrder": "12"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2245",
				"Address": "Laurence Brook",
				"Location": "Lucan Road",
				"SeqNumber": "70",
				"Latitude": "53.349464",
				"Longitude": "-6.348272",
				"SeqNumberExt": "70"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop14",
					"msdata:rowOrder": "13"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2246",
				"Address": "Chapelizod",
				"Location": "Main Street",
				"SeqNumber": "80",
				"Latitude": "53.348306",
				"Longitude": "-6.343637",
				"SeqNumberExt": "80"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop15",
					"msdata:rowOrder": "14"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2247",
				"Address": "St Mary's Hospital",
				"Location": "Chapelizod Gate",
				"SeqNumber": "90",
				"Latitude": "53.346751",
				"Longitude": "-6.336281",
				"SeqNumberExt": "90"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop16",
					"msdata:rowOrder": "15"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2248",
				"Address": "Military Road",
				"Location": "Sports Ground",
				"SeqNumber": "100",
				"Latitude": "53.346318",
				"Longitude": "-6.327864",
				"SeqNumberExt": "100"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop17",
					"msdata:rowOrder": "16"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2249",
				"Address": "Garda Boat Club",
				"Location": "Chapelizod Rd",
				"SeqNumber": "110",
				"Latitude": "53.346528",
				"Longitude": "-6.321124",
				"SeqNumberExt": "110"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop18",
					"msdata:rowOrder": "17"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2250",
				"Address": "Salmon Pool",
				"Location": "Chapelizod Rd",
				"SeqNumber": "120",
				"Latitude": "53.347435",
				"Longitude": "-6.315308",
				"SeqNumberExt": "120"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop19",
					"msdata:rowOrder": "18"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2251",
				"Address": "Islandbridge Gate",
				"Location": "Chapelizod Rd",
				"SeqNumber": "130",
				"Latitude": "53.348126",
				"Longitude": "-6.310968",
				"SeqNumberExt": "130"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop20",
					"msdata:rowOrder": "19"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "1472",
				"Address": "Conyngham Road",
				"Location": "Bridgewater House",
				"SeqNumber": "140",
				"Latitude": "53.348427",
				"Longitude": "-6.305953",
				"SeqNumberExt": "140"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop21",
					"msdata:rowOrder": "20"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "4408",
				"Address": "Phoenix House",
				"Location": "Conyngham Road",
				"SeqNumber": "150",
				"Latitude": "53.348327",
				"Longitude": "-6.301091",
				"SeqNumberExt": "150"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop22",
					"msdata:rowOrder": "21"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "1473",
				"Address": "Phoenix Park Gate",
				"Location": "Conyngham Road",
				"SeqNumber": "160",
				"Latitude": "53.348299",
				"Longitude": "-6.29853",
				"SeqNumberExt": "160"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop23",
					"msdata:rowOrder": "22"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "1474",
				"Address": "Parkgate Street",
				"Location": "Heuston Station",
				"SeqNumber": "170",
				"Latitude": "53.347944",
				"Longitude": "-6.292341",
				"SeqNumberExt": "170"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop24",
					"msdata:rowOrder": "23"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "1476",
				"Address": "Sarsfield Quay",
				"Location": "Ellis Street",
				"SeqNumber": "180",
				"Latitude": "53.347003",
				"Longitude": "-6.284664",
				"SeqNumberExt": "180"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop25",
					"msdata:rowOrder": "24"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "7453",
				"Address": "Arran Quay",
				"Location": "Ocean House",
				"SeqNumber": "190",
				"Latitude": "53.346338",
				"Longitude": "-6.278378",
				"SeqNumberExt": "190"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop26",
					"msdata:rowOrder": "25"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "1478",
				"Address": "Four Courts",
				"Location": "Chancery Place",
				"SeqNumber": "200",
				"Latitude": "53.345648",
				"Longitude": "-6.272935",
				"SeqNumberExt": "200"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop27",
					"msdata:rowOrder": "26"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "1479",
				"Address": "Ormond Quay Upper",
				"Location": "Capel Street",
				"SeqNumber": "210",
				"Latitude": "53.345988",
				"Longitude": "-6.268634",
				"SeqNumberExt": "210"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop28",
					"msdata:rowOrder": "27"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "315",
				"Address": "Bachelors Walk",
				"Location": "Liffey Street",
				"SeqNumber": "220",
				"Latitude": "53.347028",
				"Longitude": "-6.261667",
				"SeqNumberExt": "220"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop29",
					"msdata:rowOrder": "28"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "406",
				"Address": "Nassau Street",
				"Location": "South Frederick Street",
				"SeqNumber": "240",
				"Latitude": "53.342581",
				"Longitude": "-6.256093",
				"SeqNumberExt": "240"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop30",
					"msdata:rowOrder": "29"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "2810",
				"Address": "Merrion Square West",
				"Location": "Clare Street",
				"SeqNumber": "250",
				"Latitude": "53.34079",
				"Longitude": "-6.250983",
				"SeqNumberExt": "250"
			},
			{
				"attributes": {
					"diffgr:id": "InboundStop31",
					"msdata:rowOrder": "30"
				},
				"Route": "26",
				"Direction": "I",
				"StopNumber": "7387",
				"Address": "Merrion Square",
				"Location": "Merrion Street",
				"SeqNumber": "260",
				"Latitude": "53.339435",
				"Longitude": "-6.250915",
				"SeqNumberExt": "260"
			}
		],
		"OutboundStop": [
			{
				"attributes": {
					"diffgr:id": "OutboundStop1",
					"msdata:rowOrder": "0"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "7391",
				"Address": "Merrion Square",
				"Location": "Merrion Street",
				"SeqNumber": "10",
				"Latitude": "53.339097",
				"Longitude": "-6.250013",
				"SeqNumberExt": "10"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop2",
					"msdata:rowOrder": "1"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "493",
				"Address": "Merrion Sq",
				"Location": "Holles Street",
				"SeqNumber": "20",
				"Latitude": "53.339889",
				"Longitude": "-6.24736",
				"SeqNumberExt": "20"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop3",
					"msdata:rowOrder": "2"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "494",
				"Address": "Clare Street",
				"Location": "Lincoln Place",
				"SeqNumber": "30",
				"Latitude": "53.341417",
				"Longitude": "-6.251671",
				"SeqNumberExt": "30"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop4",
					"msdata:rowOrder": "3"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "495",
				"Address": "Pearse Station",
				"Location": "Westland Row",
				"SeqNumber": "40",
				"Latitude": "53.343586",
				"Longitude": "-6.249726",
				"SeqNumberExt": "40"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop5",
					"msdata:rowOrder": "4"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "400",
				"Address": "Shaw Street",
				"Location": "Pearse Street",
				"SeqNumber": "50",
				"Latitude": "53.344846",
				"Longitude": "-6.253389",
				"SeqNumberExt": "50"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop6",
					"msdata:rowOrder": "5"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "346",
				"Address": "Pearse Street",
				"Location": "Garda Station",
				"SeqNumber": "60",
				"Latitude": "53.345538",
				"Longitude": "-6.256576",
				"SeqNumberExt": "60"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop7",
					"msdata:rowOrder": "6"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "317",
				"Address": "Westmoreland Street",
				"Location": "Fleet Street",
				"SeqNumber": "70",
				"Latitude": "53.346526",
				"Longitude": "-6.259269",
				"SeqNumberExt": "70"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop8",
					"msdata:rowOrder": "7"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "312",
				"Address": "Wellington Quay",
				"Location": "Parliament Street",
				"SeqNumber": "80",
				"Latitude": "53.34547",
				"Longitude": "-6.266192",
				"SeqNumberExt": "80"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop9",
					"msdata:rowOrder": "8"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "1444",
				"Address": "Merchant's Quay",
				"Location": "Winetavern Street",
				"SeqNumber": "90",
				"Latitude": "53.345075",
				"Longitude": "-6.274513",
				"SeqNumberExt": "90"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop10",
					"msdata:rowOrder": "9"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "1445",
				"Address": "Usher's Quay",
				"Location": "Usher Street",
				"SeqNumber": "100",
				"Latitude": "53.345988",
				"Longitude": "-6.279808",
				"SeqNumberExt": "100"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop11",
					"msdata:rowOrder": "10"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "7078",
				"Address": "Parkgate Street",
				"Location": "Heuston Station",
				"SeqNumber": "110",
				"Latitude": "53.347905",
				"Longitude": "-6.292866",
				"SeqNumberExt": "110"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop12",
					"msdata:rowOrder": "11"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "1449",
				"Address": "Phoenix Park Gate",
				"Location": "Conyngham Road",
				"SeqNumber": "120",
				"Latitude": "53.348152",
				"Longitude": "-6.297884",
				"SeqNumberExt": "120"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop13",
					"msdata:rowOrder": "12"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "1450",
				"Address": "Conyngham Road",
				"Location": "Phoenix House",
				"SeqNumber": "130",
				"Latitude": "53.348149",
				"Longitude": "-6.301852",
				"SeqNumberExt": "130"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop14",
					"msdata:rowOrder": "13"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "1451",
				"Address": "Bridgewater House",
				"Location": "Conyngham Road",
				"SeqNumber": "140",
				"Latitude": "53.34828",
				"Longitude": "-6.305432",
				"SeqNumberExt": "140"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop15",
					"msdata:rowOrder": "14"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "2191",
				"Address": "Islandbridge Gate",
				"Location": "Chapelizod Rd",
				"SeqNumber": "150",
				"Latitude": "53.348026",
				"Longitude": "-6.310429",
				"SeqNumberExt": "150"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop16",
					"msdata:rowOrder": "15"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "2192",
				"Address": "UCD Boat Club",
				"Location": "Chapelizod Rd",
				"SeqNumber": "160",
				"Latitude": "53.347243",
				"Longitude": "-6.315646",
				"SeqNumberExt": "160"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop17",
					"msdata:rowOrder": "16"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "2193",
				"Address": "Garda Rowing Club",
				"Location": "Chapelizod Rd",
				"SeqNumber": "170",
				"Latitude": "53.346379",
				"Longitude": "-6.323429",
				"SeqNumberExt": "170"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop18",
					"msdata:rowOrder": "17"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "2194",
				"Address": "Military Road",
				"Location": "Sports Ground",
				"SeqNumber": "180",
				"Latitude": "53.346188",
				"Longitude": "-6.328387",
				"SeqNumberExt": "180"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop19",
					"msdata:rowOrder": "18"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "2195",
				"Address": "St Mary's Hospital",
				"Location": "Chapelizod Gate",
				"SeqNumber": "190",
				"Latitude": "53.346743",
				"Longitude": "-6.337584",
				"SeqNumberExt": "190"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop20",
					"msdata:rowOrder": "19"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "2196",
				"Address": "Chapelizod",
				"Location": "Kings Hall",
				"SeqNumber": "200",
				"Latitude": "53.3479",
				"Longitude": "-6.3416",
				"SeqNumberExt": "200"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop21",
					"msdata:rowOrder": "20"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "2197",
				"Address": "Lucan Road",
				"Location": "Chapelizod Court",
				"SeqNumber": "210",
				"Latitude": "53.348165",
				"Longitude": "-6.346729",
				"SeqNumberExt": "210"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop22",
					"msdata:rowOrder": "21"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "2198",
				"Address": "Belgrove Park",
				"Location": "Lucan Road",
				"SeqNumber": "220",
				"Latitude": "53.350624",
				"Longitude": "-6.351056",
				"SeqNumberExt": "220"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop23",
					"msdata:rowOrder": "22"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "2200",
				"Address": "Kylemore Road",
				"Location": "Chapelizod Bridge",
				"SeqNumber": "230",
				"Latitude": "53.350278",
				"Longitude": "-6.352949",
				"SeqNumberExt": "230"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop24",
					"msdata:rowOrder": "23"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "2201",
				"Address": "Palmerstown Drive",
				"Location": "Lucan Road",
				"SeqNumber": "240",
				"Latitude": "53.353295",
				"Longitude": "-6.364662",
				"SeqNumberExt": "240"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop25",
					"msdata:rowOrder": "24"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "7239",
				"Address": "The Oval",
				"Location": "Lucan Road",
				"SeqNumber": "250",
				"Latitude": "53.354058",
				"Longitude": "-6.368911",
				"SeqNumberExt": "250"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop26",
					"msdata:rowOrder": "25"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "4401",
				"Address": "Kennelsfort Road",
				"Location": "Lucan Road",
				"SeqNumber": "260",
				"Latitude": "53.354774",
				"Longitude": "-6.371766",
				"SeqNumberExt": "260"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop27",
					"msdata:rowOrder": "26"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "2202",
				"Address": "Lucan Road",
				"Location": "Kennelsfort Rd",
				"SeqNumber": "270",
				"Latitude": "53.354376",
				"Longitude": "-6.373285",
				"SeqNumberExt": "270"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop28",
					"msdata:rowOrder": "27"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "2203",
				"Address": "Palmerstown Avenue",
				"Location": "Kennelsfort Rd",
				"SeqNumber": "280",
				"Latitude": "53.3532",
				"Longitude": "-6.376135",
				"SeqNumberExt": "280"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop29",
					"msdata:rowOrder": "28"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "2204",
				"Address": "Oakcourt Avenue",
				"Location": "Kennelsfort Rd",
				"SeqNumber": "290",
				"Latitude": "53.349954",
				"Longitude": "-6.377624",
				"SeqNumberExt": "290"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop30",
					"msdata:rowOrder": "29"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "4888",
				"Address": "Palmerstown Crescent",
				"Location": "Kennelsfort Rd",
				"SeqNumber": "300",
				"Latitude": "53.347427",
				"Longitude": "-6.378912",
				"SeqNumberExt": "300"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop31",
					"msdata:rowOrder": "30"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "4798",
				"Address": "Coldcut Road",
				"Location": "Kennelsfort Road",
				"SeqNumber": "310",
				"Latitude": "53.34561",
				"Longitude": "-6.380901",
				"SeqNumberExt": "310"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop32",
					"msdata:rowOrder": "31"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "7976",
				"Address": "Liffey Valley SC",
				"Location": "Fonthill Road",
				"SeqNumber": "320",
				"Latitude": "53.352713",
				"Longitude": "-6.396079",
				"SeqNumberExt": "320"
			},
			{
				"attributes": {
					"diffgr:id": "OutboundStop33",
					"msdata:rowOrder": "32"
				},
				"Route": "26",
				"Direction": "O",
				"StopNumber": "8029",
				"Address": "Liffey Valley SC",
				"Location": "Plaza",
				"SeqNumber": "330",
				"Latitude": "53.354429",
				"Longitude": "-6.392694",
				"SeqNumberExt": "330"
			}
		]
	}
}

```
* GET: http://localhost:8000/bus/stop/{Bus_stop_id}
(Bus Stop ID eg 1474)
```
{
	"stopId": "1474",
	"departures": [
		{
			"attributes": {
				"diffgr:id": "StopData1",
				"msdata:rowOrder": "0"
			},
			"ServiceDelivery_ResponseTimestamp": "2023-03-27T20:04:15.167+01:00",
			"ServiceDelivery_ProducerRef": "bac",
			"ServiceDelivery_Status": "true",
			"ServiceDelivery_MoreData": "false",
			"StopMonitoringDelivery_Version": "2.0",
			"StopMonitoringDelivery_ResponseTimestamp": "2023-03-27T20:04:15.163+01:00",
			"StopMonitoringDelivery_RequestMessageRef": null,
			"MonitoredStopVisit_RecordedAtTime": "2023-03-27T20:04:15.167+01:00",
			"MonitoredStopVisit_MonitoringRef": "1474",
			"MonitoredVehicleJourney_LineRef": "68",
			"MonitoredVehicleJourney_DirectionRef": "Inbound",
			"FramedVehicleJourneyRef_DataFrameRef": "2023-03-27",
			"FramedVehicleJourneyRef_DatedVehicleJourneyRef": "2418",
			"MonitoredVehicleJourney_PublishedLineName": "69",
			"MonitoredVehicleJourney_OperatorRef": "bac",
			"MonitoredVehicleJourney_DestinationRef": "7665",
			"MonitoredVehicleJourney_DestinationName": "Poolbeg St",
			"MonitoredVehicleJourney_Monitored": "true",
			"MonitoredVehicleJourney_InCongestion": "false",
			"MonitoredVehicleJourney_BlockRef": "68008",
			"MonitoredVehicleJourney_VehicleRef": "44426",
			"MonitoredCall_VisitNumber": "57",
			"MonitoredCall_VehicleAtStop": "false",
			"MonitoredCall_AimedArrivalTime": "2023-03-27T20:17:05+01:00",
			"MonitoredCall_ExpectedArrivalTime": "2023-03-27T20:12:56.03+01:00",
			"MonitoredCall_AimedDepartureTime": "2023-03-27T20:17:05+01:00",
			"MonitoredCall_ExpectedDepartureTime": "2023-03-27T20:12:56.03+01:00",
			"Timestamp": "2023-03-27T20:04:15.26+01:00",
			"LineNote": null
		},
		{
			"attributes": {
				"diffgr:id": "StopData2",
				"msdata:rowOrder": "1"
			},
			"ServiceDelivery_ResponseTimestamp": "2023-03-27T20:04:15.167+01:00",
			"ServiceDelivery_ProducerRef": "bac",
			"ServiceDelivery_Status": "true",
			"ServiceDelivery_MoreData": "false",
			"StopMonitoringDelivery_Version": "2.0",
			"StopMonitoringDelivery_ResponseTimestamp": "2023-03-27T20:04:15.163+01:00",
			"StopMonitoringDelivery_RequestMessageRef": null,
			"MonitoredStopVisit_RecordedAtTime": "2023-03-27T20:04:15.167+01:00",
			"MonitoredStopVisit_MonitoringRef": "1474",
			"MonitoredVehicleJourney_LineRef": "26",
			"MonitoredVehicleJourney_DirectionRef": "Inbound",
			"FramedVehicleJourneyRef_DataFrameRef": "2023-03-27",
			"FramedVehicleJourneyRef_DatedVehicleJourneyRef": "7421",
			"MonitoredVehicleJourney_PublishedLineName": "26",
			"MonitoredVehicleJourney_OperatorRef": "bac",
			"MonitoredVehicleJourney_DestinationRef": "7387",
			"MonitoredVehicleJourney_DestinationName": "Merrion Square",
			"MonitoredVehicleJourney_Monitored": "true",
			"MonitoredVehicleJourney_InCongestion": "false",
			"MonitoredVehicleJourney_BlockRef": "26023",
			"MonitoredVehicleJourney_VehicleRef": "44521",
			"MonitoredCall_VisitNumber": "23",
			"MonitoredCall_VehicleAtStop": "false",
			"MonitoredCall_AimedArrivalTime": "2023-03-27T20:17:35+01:00",
			"MonitoredCall_ExpectedArrivalTime": "2023-03-27T20:15:23+01:00",
			"MonitoredCall_AimedDepartureTime": "2023-03-27T20:17:35+01:00",
			"MonitoredCall_ExpectedDepartureTime": "2023-03-27T20:15:23+01:00",
			"Timestamp": "2023-03-27T20:04:15.277+01:00",
			"LineNote": null
		},
		{
			"attributes": {
				"diffgr:id": "StopData3",
				"msdata:rowOrder": "2"
			},
			"ServiceDelivery_ResponseTimestamp": "2023-03-27T20:04:15.167+01:00",
			"ServiceDelivery_ProducerRef": "bac",
			"ServiceDelivery_Status": "true",
			"ServiceDelivery_MoreData": "false",
			"StopMonitoringDelivery_Version": "2.0",
			"StopMonitoringDelivery_ResponseTimestamp": "2023-03-27T20:04:15.163+01:00",
			"StopMonitoringDelivery_RequestMessageRef": null,
			"MonitoredStopVisit_RecordedAtTime": "2023-03-27T20:04:15.167+01:00",
			"MonitoredStopVisit_MonitoringRef": "1474",
			"MonitoredVehicleJourney_LineRef": "26",
			"MonitoredVehicleJourney_DirectionRef": "Inbound",
			"FramedVehicleJourneyRef_DataFrameRef": "2023-03-27",
			"FramedVehicleJourneyRef_DatedVehicleJourneyRef": "7409",
			"MonitoredVehicleJourney_PublishedLineName": "26",
			"MonitoredVehicleJourney_OperatorRef": "bac",
			"MonitoredVehicleJourney_DestinationRef": "7387",
			"MonitoredVehicleJourney_DestinationName": "Merrion Square",
			"MonitoredVehicleJourney_Monitored": "true",
			"MonitoredVehicleJourney_InCongestion": "false",
			"MonitoredVehicleJourney_BlockRef": "26020",
			"MonitoredVehicleJourney_VehicleRef": "47002",
			"MonitoredCall_VisitNumber": "23",
			"MonitoredCall_VehicleAtStop": "false",
			"MonitoredCall_AimedArrivalTime": "2023-03-27T20:32:35+01:00",
			"MonitoredCall_ExpectedArrivalTime": "2023-03-27T20:20:50.567+01:00",
			"MonitoredCall_AimedDepartureTime": "2023-03-27T20:32:35+01:00",
			"MonitoredCall_ExpectedDepartureTime": "2023-03-27T20:20:50.567+01:00",
			"Timestamp": "2023-03-27T20:04:15.277+01:00",
			"LineNote": null
		},
		{
			"attributes": {
				"diffgr:id": "StopData4",
				"msdata:rowOrder": "3"
			},
			"ServiceDelivery_ResponseTimestamp": "2023-03-27T20:04:15.167+01:00",
			"ServiceDelivery_ProducerRef": "bac",
			"ServiceDelivery_Status": "true",
			"ServiceDelivery_MoreData": "false",
			"StopMonitoringDelivery_Version": "2.0",
			"StopMonitoringDelivery_ResponseTimestamp": "2023-03-27T20:04:15.163+01:00",
			"StopMonitoringDelivery_RequestMessageRef": null,
			"MonitoredStopVisit_RecordedAtTime": "2023-03-27T20:04:15.167+01:00",
			"MonitoredStopVisit_MonitoringRef": "1474",
			"MonitoredVehicleJourney_LineRef": "26",
			"MonitoredVehicleJourney_DirectionRef": "Inbound",
			"FramedVehicleJourneyRef_DataFrameRef": "2023-03-27",
			"FramedVehicleJourneyRef_DatedVehicleJourneyRef": "7298",
			"MonitoredVehicleJourney_PublishedLineName": "26",
			"MonitoredVehicleJourney_OperatorRef": "bac",
			"MonitoredVehicleJourney_DestinationRef": "7387",
			"MonitoredVehicleJourney_DestinationName": "Merrion Square",
			"MonitoredVehicleJourney_Monitored": "true",
			"MonitoredVehicleJourney_InCongestion": "false",
			"MonitoredVehicleJourney_BlockRef": "26004",
			"MonitoredVehicleJourney_VehicleRef": null,
			"MonitoredCall_VisitNumber": "23",
			"MonitoredCall_VehicleAtStop": "false",
			"MonitoredCall_AimedArrivalTime": "2023-03-27T20:47:35+01:00",
			"MonitoredCall_ExpectedArrivalTime": "2023-03-27T20:47:35+01:00",
			"MonitoredCall_AimedDepartureTime": "2023-03-27T20:47:35+01:00",
			"MonitoredCall_ExpectedDepartureTime": "2023-03-27T20:47:35+01:00",
			"Timestamp": "2023-03-27T20:04:15.293+01:00",
			"LineNote": null
		},
		{
			"attributes": {
				"diffgr:id": "StopData5",
				"msdata:rowOrder": "4"
			},
			"ServiceDelivery_ResponseTimestamp": "2023-03-27T20:04:15.167+01:00",
			"ServiceDelivery_ProducerRef": "bac",
			"ServiceDelivery_Status": "true",
			"ServiceDelivery_MoreData": "false",
			"StopMonitoringDelivery_Version": "2.0",
			"StopMonitoringDelivery_ResponseTimestamp": "2023-03-27T20:04:15.163+01:00",
			"StopMonitoringDelivery_RequestMessageRef": null,
			"MonitoredStopVisit_RecordedAtTime": "2023-03-27T20:04:15.167+01:00",
			"MonitoredStopVisit_MonitoringRef": "1474",
			"MonitoredVehicleJourney_LineRef": "68",
			"MonitoredVehicleJourney_DirectionRef": "Inbound",
			"FramedVehicleJourneyRef_DataFrameRef": "2023-03-27",
			"FramedVehicleJourneyRef_DatedVehicleJourneyRef": "3073",
			"MonitoredVehicleJourney_PublishedLineName": "69",
			"MonitoredVehicleJourney_OperatorRef": "bac",
			"MonitoredVehicleJourney_DestinationRef": "7665",
			"MonitoredVehicleJourney_DestinationName": "Poolbeg St",
			"MonitoredVehicleJourney_Monitored": "true",
			"MonitoredVehicleJourney_InCongestion": "false",
			"MonitoredVehicleJourney_BlockRef": "68001",
			"MonitoredVehicleJourney_VehicleRef": "44522",
			"MonitoredCall_VisitNumber": "57",
			"MonitoredCall_VehicleAtStop": "false",
			"MonitoredCall_AimedArrivalTime": "2023-03-27T21:02:05+01:00",
			"MonitoredCall_ExpectedArrivalTime": "2023-03-27T21:02:05+01:00",
			"MonitoredCall_AimedDepartureTime": "2023-03-27T21:02:05+01:00",
			"MonitoredCall_ExpectedDepartureTime": "2023-03-27T21:02:05+01:00",
			"Timestamp": "2023-03-27T20:04:15.293+01:00",
			"LineNote": null
		}
	]
}
```
