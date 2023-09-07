import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as MapConstants from './map.constants';
import * as L from 'leaflet';
import 'leaflet.polyline.snakeanim';
import * as Papa from 'papaparse';

// Define interface to extend LatLng with subtract and normalize methods
declare module 'leaflet' {
  interface LatLng {
    subtract(otherPoint: LatLngExpression): LatLng;
    normalize(): LatLng;
    add(otherPoint: LatLngExpression): LatLng;
    multiplyBy(scale: number): LatLng;
  }
}

@Component({
  selector: 'map2',
  templateUrl: './map2.component.html',
  styleUrls: ['map2.component.css',],
})
export class Map2Component implements OnInit {
  public map: L.Map;
  private busRoute: L.Polyline;
  private luasRoute: L.Polyline;
  public busRoutes: { name: string, coordinates: [number, number][] }[] = [];
  public luasRoutes: { name: string, coordinates: [number, number][] }[] = [];
  private taxiRoutes: {
    name: string;
    coordinates: [number, number][];
    taxiDrawnRoute?: L.Polyline; 
    taxiMarker?: L.Marker;
  }[] = [];  
  public taxiPositions: { name: string; lon: number; lat: number }[] = [];
  private bikeStopsLayer: L.LayerGroup = L.layerGroup(); // Define layer group to hold markers
  private cctvLayer: L.LayerGroup = L.layerGroup();
  private tweetLayer: L.LayerGroup=L.layerGroup();
  private clusterLayer: L.LayerGroup = L.layerGroup(); 
  clusterMessage: string = '';
  private clustersVisible = true; 
  tweetRecommendationMessage: string='';
  tweetTimestamp: string='';
  tweetPostMessage: string='';
  tweetDisplay: string='';
  private tweetVisible = true; 
  selectedBusRoute: { name: string, coordinates: [number, number][] };
  selectedLuasRoute: { name: string, coordinates: [number, number][] }
  public busStopsByRoute: { [routeShortName: string]: any[] } = {};
  private busStopMarkers: L.Marker[] = [];
  public luasStopsByRoute: { [routeShortName: string]: any[] } = {};
  private luasStopMarkers: L.Marker[] = [];
  private taxiIcon = L.icon({
    iconUrl: MapConstants.iconUrl, // Replace this with the path to your taxi icon image file
    iconSize: [12, 20],
    iconAnchor: [6, 20], 
  });  
  private taxiMovementTimerId: { [taxiRouteName: string]: number } = {};
  constructor(private http: HttpClient) {}

  public simulateAllTaxiMovements() {
    let updatedTaxisCount = 0;
 
    this.taxiRoutes.forEach((taxiRoute) => {
      const coordinates = taxiRoute.coordinates;
      const lastIndex = coordinates.length - 1;
      let index = 0;
  
      taxiRoute.taxiMarker = L.marker(coordinates[0], { icon: this.taxiIcon }).addTo(this.map).bindPopup(taxiRoute.name, { offset: [0, -20] });
      // In the simulateAllTaxiMovements method, inside the forEach loop for this.taxiRoutes
      taxiRoute.taxiDrawnRoute = L.polyline([], { color: 'green', weight: 5, opacity: 0.7 }).addTo(this.map);

  
      const updateTaxiPosition = () => {
        if (index < lastIndex) {
          taxiRoute.taxiMarker?.setLatLng(coordinates[index]);
          taxiRoute.taxiDrawnRoute?.addLatLng(coordinates[index]);
          const currentPosition = {
            name: taxiRoute.name,
            lon: coordinates[index][1],
            lat: coordinates[index][0],
          };
          this.taxiPositions.push(currentPosition);
          index++;
          const timerId = window.setTimeout(updateTaxiPosition, 5000);
          this.taxiMovementTimerId[taxiRoute.name] = timerId; // Add this line
          updatedTaxisCount++;
        } else {
          console.log('Taxi movement simulation completed for', taxiRoute.name);
          taxiRoute.taxiMarker?.removeFrom(this.map);
          taxiRoute.taxiDrawnRoute?.removeFrom(this.map);
        }
      };
  
      updateTaxiPosition();
    });
  }

  public sendCurrentTaxiPositions(): void {
    // Assuming taxiPositions is now a class member
    if (this.taxiPositions.length > 0) {
      this.sendTaxiPositionsToBackend(this.taxiPositions);
    } else {
      console.log('No taxi positions available to send.');
    }
  }  

  private sendTaxiPositionsToBackend(taxiPositions: { name: string; lon: number; lat: number }[]): void {
    const apiUrl = MapConstants.backendTaxiUrl; // Replace this with your backend API endpoint URL
  
    this.http.post(apiUrl, { taxis: taxiPositions }).subscribe(
      (clusterData: any)  => {
        this.clusterMessage = clusterData.message;
        this.addClustersToMap(clusterData);
        console.log('Taxi positions sent successfully');
      },
      (error) => {
        console.error('Error sending taxi positions:', error);
      }
    );
  } 
  
  ngOnInit() {
    
    this.map = L.map('map', {
      center: [53.347135, -6.258937],
      zoom: 13,
    });

    L.tileLayer(MapConstants.mapUrl, {
      maxZoom: 18,
      minZoom: 10,
      attribution:
       MapConstants.mapAtribution,
    }).addTo(this.map);

    this.http.get(MapConstants.geojsonUrl_bus).subscribe((geojson: any) => {
      const featuresByRouteShortName: { [routeShortName: string]: any[] } = {};
      
      geojson.features.forEach((feature: any) => {
        if (feature.geometry.type === 'LineString') {
          const routeShortName = feature.properties.route_short_name;
          if (!featuresByRouteShortName[routeShortName]) {
            featuresByRouteShortName[routeShortName] = [];
          }
          featuresByRouteShortName[routeShortName].push(feature);
        } else if (feature.geometry.type === 'Point' && feature.properties.stop_code) {
          const routeShortNames = feature.properties.routes.map((route: any) => route.route_short_name);
          routeShortNames.forEach((routeShortName: string) => {
            if (!this.busStopsByRoute[routeShortName]) {
              this.busStopsByRoute[routeShortName] = [];
            }
            this.busStopsByRoute[routeShortName].push(feature);
          });
        }
      });
      
    
      this.busRoutes = Object.values(featuresByRouteShortName).map((features: any[]) => {
        const longestFeature = features.reduce((longest: any, current: any) =>
          current.geometry.coordinates.length > longest.geometry.coordinates.length ? current : longest, features[0]);
    
        return {
          name: longestFeature.properties.route_short_name,
          coordinates: longestFeature.geometry.coordinates.map((coord: number[]) => [coord[1], coord[0]]),
        };
      });
      
   /*    this.selectedBusRoute = this.busRoutes[0];
      this.showBusRoute(); */
    });

    this.http.get(MapConstants.geojsonUrl_luas).subscribe((geojson: any) => {
      const featuresByRouteShortName: { [routeShortName: string]: any[] } = {};
      
      geojson.features.forEach((feature: any) => {
        if (feature.geometry.type === 'LineString') {
          const routeShortName = feature.properties.route_short_name;
          if (!featuresByRouteShortName[routeShortName]) {
            featuresByRouteShortName[routeShortName] = [];
          }
          featuresByRouteShortName[routeShortName].push(feature);
        } else if (feature.geometry.type === 'Point' && feature.properties.stop_id) {
          const routeShortNames = feature.properties.routes.map((route: any) => route.route_short_name);
          routeShortNames.forEach((routeShortName: string) => {
            if (!this.luasStopsByRoute[routeShortName]) {
              this.luasStopsByRoute[routeShortName] = [];
            }
            this.luasStopsByRoute[routeShortName].push(feature);
          });
        }
      });
      
    
      this.luasRoutes = Object.values(featuresByRouteShortName).map((features: any[]) => {
        const longestFeature = features.reduce((longest: any, current: any) =>
          current.geometry.coordinates.length > longest.geometry.coordinates.length ? current : longest, features[0]);
    
        return {
          name: longestFeature.properties.route_short_name,
          coordinates: longestFeature.geometry.coordinates.map((coord: number[]) => [coord[1], coord[0]]),
        };
      });
      
/*       this.selectedLuasRoute = this.luasRoutes[0];
      this.showLuasRoute(); */
    });

    this.http.get(MapConstants.geojsonUrl_taxi).subscribe((geojson: any) => {
      const featuresByName: { [taxi: string]: any } = {};
      geojson.features.forEach((feature: any) => {
        const taxiName = feature.properties.taxi;
        featuresByName[taxiName] = feature;
      });

      this.taxiRoutes = Object.keys(featuresByName).map((taxiName: string) => {
        const feature = featuresByName[taxiName];
        return {
          name: taxiName,
          coordinates: feature.geometry.coordinates.map((coord: number[]) => [coord[1], coord[0]]),
        };
      });
     
/*       // Set the selected taxi route to the first one in the array
      this.selectedTaxiRoute = this.taxiRoutes[0];
      // Call the showTaxiRoute function to display the route on the map
      this.showTaxiRoute(); */
    });

    interface BikeStop {
      Number: number;
      Latitude: number;
      Longitude: number;
      Name: string;
      Address: string;
    }


    this.http.get(MapConstants.csvUrl_bike, { responseType: 'text' }).subscribe(csvString => {
      // Use PapaParse to convert string to array of objects
      const data = Papa.parse(csvString, { header: true, dynamicTyping: true }).data;
    
      // For each row in data, create a marker and add it to the layer group
      // For each row, columns `Latitude`, `Longitude`, and `Title` are required
      for (const row of data as BikeStop[]) {
        this.http.get(MapConstants.API_ENDPOINT+`getBike/${row.Number}`).subscribe((json: any) => {
        const biks_stands= json.bike_stands;
        const address=json.address;
        const available_bikes=json.available_bikes;
        const status=json.status;
        const prediction=json.prediction;
        let popupHtml_bike = `<b>Bike Stop Name:</b> ${address}<br>
                              <b>Bike Stands:</b> ${biks_stands}<br>
                              <b>Available Bikes:</b> ${available_bikes}<br>
                              <b>Status:</b> ${status}<br>
                              <b>Predicted no. of bikes after 1 hour:</b> ${prediction}<br><br>`;
        const marker = L.marker([row.Latitude, row.Longitude], {
          icon: L.icon({
            iconUrl: MapConstants.iconUrl,
            iconSize: [12, 20],
            iconAnchor: [6, 20],
            popupAnchor: [1, -34],
          }),
        }).bindPopup(popupHtml_bike);
        
        marker.addTo(this.bikeStopsLayer);
      });
      }
    });

    //this.loadClusterData(); // Load cluster data from the backend
    //this.clusterLayer.addTo(this.map); // Add the cluster layer to the map
    
  }

/*     private loadClusterData() {
      // Load data from your local .geojson file
      this.http.get('/assets/map/cluster.geojson').subscribe((clusterData: any) => {
        this.clusterMessage = clusterData.message;
        this.addClustersToMap(clusterData);
      });
    } */
    

    addClustersToMap(clusterData: any) {
      const clusterFeatures = clusterData.features;

      clusterFeatures.forEach((feature: any) => {
        const clusterType = feature.properties.cluster_type;
        const coordinates = feature.geometry.coordinates;

        const latLngs = coordinates.map((coord: [number, number]) => L.latLng(coord[1], coord[0]));

        const clusterPolyline = L.polyline(latLngs, {
          color: clusterType.startsWith('High Density') ? 'red' : 'blue',
          weight: 3,
        });

        clusterPolyline.bindPopup(clusterType);
        this.clusterLayer.addLayer(clusterPolyline); // Add the polyline to the cluster layer
      });
    }

    public toggleClusters():void {
      const messageContainer = document.querySelector<HTMLElement>('.message-container1');
      this.clustersVisible = !this.clustersVisible;
    
      if (this.clustersVisible) {
        // show clusters and message container
        if (messageContainer) {
          messageContainer.hidden = false;
        }
        this.sendCurrentTaxiPositions();
        this.clusterLayer.addTo(this.map);
      } else {
        // hide clusters and message container
        if (messageContainer) {
          messageContainer.hidden = true;
        }
        this.clusterLayer.clearLayers();
        this.clusterLayer.removeFrom(this.map);
      }
    }
    
    private loadTweetData() {
      // Load data from your local .geojson file
      this.http.get(MapConstants.tweetUrl).subscribe((tweetData: any) => {
        this.tweetRecommendationMessage = tweetData.message;
        this.tweetTimestamp=tweetData.TimeStamp;
        this.tweetPostMessage=tweetData.incident;
        this.addTweetToMap(tweetData);
      });
    }
    

    addTweetToMap(tweetData: any) {
      const tweetFeatures = tweetData.features;

      tweetFeatures.forEach((feature: any) => {
        const tweetType = feature.properties.plot_type;
        const coordinates = feature.geometry.coordinates;

        const latLngs = coordinates.map((coord: [number, number]) => L.latLng(coord[1], coord[0]));

        const tweetPolyline = L.polyline(latLngs, {
          color: tweetType.startsWith('Incident') ? 'black' : 'green',
          weight: 3,
        });

        tweetPolyline.bindPopup(tweetType);
        this.tweetLayer.addLayer(tweetPolyline); // Add the polyline to the cluster layer
      });
    }

    public toggleTweet():void {
      const messageContainer1 = document.querySelector<HTMLElement>('.message-container2');
      this.tweetVisible = !this.tweetVisible;
    
      if (this.tweetVisible) {
        if (messageContainer1) {
          messageContainer1.hidden = false;
        }
        this.loadTweetData();
        this.tweetLayer.addTo(this.map);
      } else {
        // hide clusters and message container
        if (messageContainer1) {
          messageContainer1.hidden = true;
        }
        this.tweetLayer.clearLayers();
        this.tweetLayer.removeFrom(this.map);
      }
    }

  showBusStops() {
    this.busStopMarkers.forEach((marker) => marker.removeFrom(this.map));
    this.busStopMarkers = [];
    const selectedRouteShortName = this.selectedBusRoute.name;
    const stopsForRoute = this.busStopsByRoute[selectedRouteShortName] || [];
  
    stopsForRoute.forEach((busStop: any) => {
      const lat = busStop.geometry.coordinates[1];
      const lon = busStop.geometry.coordinates[0];
      const stopName = busStop.properties.stop_name;
      const stopId = busStop.properties.stop_code;
  
      // Retrieve departure information from API for this stop
      const apiEndpoint = MapConstants.API_ENDPOINT+`bus/stop/${stopId}`;
      this.http.get(apiEndpoint).subscribe((json: any) => {
        const departures = json.departures;
        let popupHtml = `<b>Stop Name:</b> ${stopName}<br><b>Stop ID:</b> ${stopId}<br><br>`;
  
        if (departures.length > 0) {
          popupHtml += '<b>Next departures:</b><br>';
        } else {
          popupHtml += '<b>No upcoming departures.</b>';
        }
  
        departures.some((departure: any) => {
          const lineRef = departure.MonitoredVehicleJourney_LineRef;
          const destinationName = departure.MonitoredVehicleJourney_DestinationName;
          const direction=departure.MonitoredVehicleJourney_DirectionRef;
          const congestion=departure.MonitoredVehicleJourney_InCongestion;
          const expectedArrivalTime = departure.MonitoredCall_ExpectedArrivalTime;
          const formattedArrivalTime = expectedArrivalTime.substring(11, 19);
          const expectedDepartureTime = departure.MonitoredCall_ExpectedDepartureTime;
          const formattedArrivalTime1 = expectedDepartureTime.substring(11, 19);
          const aimedArrivalTime = departure.MonitoredCall_AimedArrivalTime;
          const formattedArrivalTime2 = aimedArrivalTime.substring(11, 19);
          const aimedDepartureTime = departure.MonitoredCall_AimedDepartureTime;
          const formattedArrivalTime3 = aimedDepartureTime.substring(11, 19);
  
          if (lineRef === selectedRouteShortName) {
            popupHtml += `<b>${destinationName}</b><br>`;
            popupHtml += `Direction: ${direction}<br>`;
            popupHtml += `Congestion: ${congestion}<br>`;
            /* popupHtml += `   `; */
            popupHtml += `Expected arrival time: ${formattedArrivalTime}<br>`;
            /* popupHtml += `   `; */
            popupHtml += `Expected departure time: ${formattedArrivalTime1}<br>`;
            /* popupHtml += `   `; */
            popupHtml += `Scheduled arrival time: ${formattedArrivalTime2}<br>`;
            /* popupHtml += `   `; */
            popupHtml += `Scheduled departure time: ${formattedArrivalTime3}<br><br>`;
            return true;
          }
          return false;
        });
  
        const marker = L.marker([lat, lon], {
          icon: L.icon({
            iconUrl: MapConstants.iconUrl,
            iconSize: [12, 20],
            iconAnchor: [6, 20],
            popupAnchor: [1, -34],
          }),
        })
          .addTo(this.map)
          .bindPopup(popupHtml);
        
        this.busStopMarkers.push(marker);
      });
    });
  }

  public toggleBikeStops(): void {
    if (this.map.hasLayer(this.bikeStopsLayer)) {
      this.map.removeLayer(this.bikeStopsLayer);
      
    } else {
      this.bikeStopsLayer.addTo(this.map);
      
    }
  }  

  public toggleCctvStops(): void {
    if (this.map.hasLayer(this.cctvLayer)) {
      this.map.removeLayer(this.cctvLayer);
      
    } else {
      this.cctvLayer.addTo(this.map);
      interface cctcLocation {
        Latitude: number;
        Longitude: number;
        Link: string;
        Name: string;
        id: string;
      }
      this.http.get(MapConstants.csvUrl_cctv, { responseType: 'text' }).subscribe(csvString1 => {
        // Use PapaParse to convert string to array of objects
        const data = Papa.parse(csvString1, { header: true, dynamicTyping: true }).data;
      
        // For each row in data, create a marker and add it to the layer group
        // For each row, columns `Latitude`, `Longitude`, and `Title` are required
        for (const row of data as cctcLocation[]) {
          this.http.get(MapConstants.API_ENDPOINT+`getCctv/${row.id}`).subscribe((json: any) => {
            this.http.get(row.Link, { responseType: 'blob' }).subscribe(imageBlob => {
              const jam=json.traffic_classification
              const backgroundColor = jam === MapConstants.JAM? 'red' : 'lightgreen';
              // Create a URL for the image blob
              const imageUrl = URL.createObjectURL(imageBlob);
              // Create a marker with a popup that includes the image
              const marker = L.marker([row.Latitude, row.Longitude], {
                icon: L.icon({
                  iconUrl: MapConstants.iconUrl,
                  iconSize: [12, 20],
                  iconAnchor: [6, 20],
                  popupAnchor: [1, -34],
                }),
              }).bindPopup(`<div style="background-color: ${backgroundColor}; padding: 10px;">
              <img src="${imageUrl}" style="max-width: 200px;">
              <br>${row.Name}</br>
              <br><b>Traffic Status:</b>${jam}</br>
            </div>`
              );
              // Add the marker to the layer group
              marker.addTo(this.cctvLayer);
            });
          });
        }
      });
    }
  }  

  
  showBusRoute() {
    if (this.busRoute) {
      this.busRoute.removeFrom(this.map);
    }

    const coordinates = this.selectedBusRoute.coordinates.map((coord: [number, number]) => L.latLng(coord[0], coord[1]));
    this.busRoute = L.polyline(coordinates, {
      color: 'red',
      weight: 5,
      opacity: 0.7,
    }).addTo(this.map);

  this.map.fitBounds(this.busRoute.getBounds(), { padding: [50, 50] });
  this.showBusStops();

  }

  showLuasStops() {
    this.luasStopMarkers.forEach((marker) => marker.removeFrom(this.map));
    this.luasStopMarkers = [];
  
    const selectedRouteShortName = this.selectedLuasRoute.name;
    const stopsForRoute = this.luasStopsByRoute[selectedRouteShortName] || [];
  
    stopsForRoute.forEach((luasStop: any) => {
      const lat = luasStop.geometry.coordinates[1];
      const lon = luasStop.geometry.coordinates[0];
      const stopName = luasStop.properties.stop_name;
      const shortName = luasStop.properties.shortName;
  
      const luasApiEndpoint = MapConstants.API_ENDPOINT + `luas/stop/${shortName}`;
      this.http.get(luasApiEndpoint).subscribe((json: any) => {
        const departuresStop = json.stop;
        let popupHtml = `<b>Stop Name:</b> ${stopName}<br>`;
  
        if (departuresStop === stopName) {
          const departureDirection = json.direction;
          if (departureDirection.length > 0) {
            popupHtml += '<b>Next departures:</b><br>';
          } else {
            popupHtml += '<b>No upcoming departures.</b>';
          }
  
          departureDirection.forEach((direction: any) => {
            const directionName = direction.name;
            const trams = direction.tram;
  
            popupHtml += `<b>${directionName}</b><br>`;
  
            trams.forEach((tram: any) => {
              const destination = tram.destination;
              const dueMins = tram.dueMins;
  
              popupHtml += `Destination: ${destination}<br>`;
              popupHtml += `Due in: ${dueMins} min(s)<br><br>`;
            });
          });
        } else {
          popupHtml += '<b>No upcoming departures.</b>';
        }
  
        const marker = L.marker([lat, lon], {
          icon: L.icon({
            iconUrl: MapConstants.iconUrl,
            iconSize: [12, 20],
            iconAnchor: [6, 20],
            popupAnchor: [1, -34],
          }),
        })
          .addTo(this.map)
          .bindPopup(popupHtml);
        this.luasStopMarkers.push(marker);
      });
    });
  }
  
  
  showLuasRoute() {
    if (this.luasRoute) {
      this.luasRoute.removeFrom(this.map);
    }

    const coordinates = this.selectedLuasRoute.coordinates.map((coord: [number, number]) => L.latLng(coord[0], coord[1]));
    this.luasRoute = L.polyline(coordinates, {
      color: 'blue',
      weight: 5,
      opacity: 0.7,
    }).addTo(this.map);

  this.map.fitBounds(this.luasRoute.getBounds(), { padding: [50, 50] });
  this.showLuasStops();

  }

  public showAllTaxiRoutes(): void {
    // Clear any ongoing taxi movement simulations.
    Object.values(this.taxiMovementTimerId).forEach(timerId => clearTimeout(timerId));
  
    // Remove the previously drawn routes and markers, if any.
    this.taxiRoutes.forEach(taxiRoute => {
      taxiRoute.taxiDrawnRoute?.removeFrom(this.map);
      taxiRoute.taxiMarker?.removeFrom(this.map);
    });
  
    // Call the simulateAllTaxiMovements method to start the simulation.
    this.simulateAllTaxiMovements();
  }
  

  
}

