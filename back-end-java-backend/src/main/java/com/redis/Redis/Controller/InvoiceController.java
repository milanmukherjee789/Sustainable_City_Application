package com.redis.Redis.Controller;
import java.io.IOException;
import java.net.ConnectException;

import org.springframework.beans.factory.annotation.Value;
import redis.clients.jedis.Jedis;
import java.util.ArrayList;
import java.util.Date;

import java.util.List;

import javax.annotation.Generated;
import javax.annotation.Resource;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

import com.redis.Redis.Entity.Invoice;
import com.redis.Redis.Entity.Recommendation;
import com.redis.Redis.Service.InvoiceService;
import com.redis.Redis.Service.RecommendationService;
import com.redis.Redis.Util.JwtUtil;

@RestController
@RequestMapping("/request")
public class InvoiceController {

	@Autowired
	InvoiceService invoiceService;
	
	@CrossOrigin
	@PostMapping("/saveUser")
	public Invoice saveInvoice(@RequestBody Invoice inv) {
		return invoiceService.saveInvoice(inv);
	}
	
	@CrossOrigin
	@GetMapping("/allUsers")
	public ResponseEntity<List<Invoice>> getAllInvoices() {
		return ResponseEntity.ok(invoiceService.getAllInvoices());
	}
	
	@CrossOrigin
	@GetMapping("/getOne/{id}")
	public Invoice getOneInvoice(@PathVariable Integer id) {
		return invoiceService.getOneInvoice(id);
	}
	 
	@CrossOrigin
	@PutMapping("/modify/{id}")
	public Invoice updateInvoice(@RequestBody Invoice inv, @PathVariable Integer id) {
		return invoiceService.updateInvoice(inv, id);
	}

	@CrossOrigin
	@DeleteMapping("/delete/{id}")
	public String deleteInvoice(@PathVariable Integer id) {
		invoiceService.deleteInvoice(id);
		return "User with id: " + id + " Deleted !";
	}
	
	@SuppressWarnings("unchecked")
	@CrossOrigin
	@PostMapping("/authenticate")
	public ResponseEntity<?> authenticateUser(@RequestBody Invoice userCredentials) {
	    List<Invoice> invoices = invoiceService.getAllInvoices();

	    for (Invoice invoice : invoices) {
	        if (invoice.getUserName().equals(userCredentials.getUserName()) &&
	            invoice.getPassWord().equals(userCredentials.getPassWord())) {
	            String token = JwtUtil.generateToken(userCredentials.getUserName());
	            JSONObject responseBody = new JSONObject();
	            responseBody.put("authorized", true);
	            responseBody.put("token", token);
	            return ResponseEntity.ok(responseBody);
	        }
	    }
	    
	    JSONObject responseBody = new JSONObject();
	    responseBody.put("authorized", false);
	    responseBody.put("token", "");
	    return ResponseEntity.ok(responseBody);
	}

	
	@Resource
	private StringRedisTemplate template;
	
	@Value("${luas.api.url}")
	private String luasApiUrl;
	private String luasRedisKeyPrefix = "luas_";
	@CrossOrigin
	@GetMapping("/luas/stop/{stop}")
	public JSONObject getLuasDetails(@PathVariable String stop) throws IOException, ParseException {
	    String LUAS_URL = luasApiUrl + stop;
	    String redisKey = luasRedisKeyPrefix + stop;
	    RestTemplate restTemplate = new RestTemplate();

	    try {
	        ResponseEntity<String> responseEntity = restTemplate.getForEntity(LUAS_URL, String.class);
	        if (responseEntity.getStatusCode() == HttpStatus.OK) {
	            String response = responseEntity.getBody();
	            redisTemplate.opsForValue().set(redisKey, response);
	            JSONParser parser = new JSONParser();
	            JSONObject dataObj = (JSONObject) parser.parse(response);
	            return dataObj;
	        } else if (responseEntity.getStatusCode() == HttpStatus.INTERNAL_SERVER_ERROR) {
	            String redisData = redisTemplate.opsForValue().get(redisKey);
	            if (redisData != null) {
	                JSONParser parser = new JSONParser();
	                JSONObject dataObj = (JSONObject) parser.parse(redisData);
	                return dataObj;
	            }
	        }

	        // If the response code is not 200 OK or 500 Internal Server Error, return an error response
	        JSONObject errorResponse = new JSONObject();
	        errorResponse.put("status", responseEntity.getStatusCodeValue());
	        errorResponse.put("error", responseEntity.getStatusCode().getReasonPhrase());
	        return errorResponse;

	    } catch (ResourceAccessException e) {
	        // Handle the exception by retrieving the latest data from Redis
	        String redisData = redisTemplate.opsForValue().get(redisKey);
	        if (redisData != null) {
	            JSONParser parser = new JSONParser();
	            JSONObject dataObj = (JSONObject) parser.parse(redisData);
	            return dataObj;
	        }

	        // If there is no cached data, return an error response
	        JSONObject errorResponse = new JSONObject();
	        errorResponse.put("status", "Connection Error");
	        errorResponse.put("error", "Error connecting to the server.");
	        return errorResponse;
	    }
	}
	

	@Autowired
	private RedisTemplate<String, String> redisTemplate;

	@Value("${redis.key.prefix.bus}")
	private String busRedisKeyPrefix;
	
	@Value("${bus.api.url}")
	private String busDetailsUrl;
	
	@CrossOrigin
	@GetMapping("/bus/stop/{stop}")
	public JSONObject getBusDetails(@PathVariable String stop) throws ParseException {
	    String BUS_URL = busDetailsUrl + stop;
	    String redisKey = busRedisKeyPrefix + stop;
	    RestTemplate restTemplate = new RestTemplate();

	    try {
	        ResponseEntity<String> responseEntity = restTemplate.getForEntity(BUS_URL, String.class);
	        if (responseEntity.getStatusCode() == HttpStatus.OK) {
	            String response = responseEntity.getBody();
	            redisTemplate.opsForValue().set(redisKey, response);
	            JSONParser parser = new JSONParser();
	            JSONObject dataObj = (JSONObject) parser.parse(response);
	            return dataObj;
	        } else if (responseEntity.getStatusCode() == HttpStatus.INTERNAL_SERVER_ERROR) {
	            String redisData = redisTemplate.opsForValue().get(redisKey);
	            if (redisData != null) {
	                JSONParser parser = new JSONParser();
	                JSONObject dataObj = (JSONObject) parser.parse(redisData);
	                return dataObj;
	            }
	        }

	        // If the response code is not 200 OK or 500 Internal Server Error, return an error response
	        JSONObject errorResponse = new JSONObject();
	        errorResponse.put("status", responseEntity.getStatusCodeValue());
	        errorResponse.put("error", responseEntity.getStatusCode().getReasonPhrase());
	        return errorResponse;

	    } catch (ResourceAccessException e) {
	        // Handle the exception by retrieving the latest data from Redis
	        String redisData = redisTemplate.opsForValue().get(redisKey);
	        if (redisData != null) {
	            JSONParser parser = new JSONParser();
	            JSONObject dataObj = (JSONObject) parser.parse(redisData);
	            return dataObj;
	        }

	        // If there is no cached data, return an error response
	        JSONObject errorResponse = new JSONObject();
	        errorResponse.put("status", "Connection Error");
	        errorResponse.put("error", "Error connecting to the server.");
	        return errorResponse;
	    }
	}
	
	@Value("${cctv.api.url}")
	private String cctvDetailsUrl;
	private String cctvRedisKeyPrefix = "cctv_";
	@CrossOrigin
	@GetMapping("/getCctv/{id}")
	public JSONObject getCCTVDetails(@PathVariable Integer id) throws IOException, ParseException {
	    String CCTV_URL = cctvDetailsUrl + id;
	    String redisKey = cctvRedisKeyPrefix + id.toString();
	    RestTemplate restTemplate = new RestTemplate();

	    try {
	        ResponseEntity<String> responseEntity = restTemplate.getForEntity(CCTV_URL, String.class);
	        if (responseEntity.getStatusCode() == HttpStatus.OK) {
	            String response = responseEntity.getBody();
	            redisTemplate.opsForValue().set(redisKey, response);
	            JSONParser parser = new JSONParser();
	            JSONObject dataObj = (JSONObject) parser.parse(response);
	            return dataObj;
	        } else if (responseEntity.getStatusCode() == HttpStatus.INTERNAL_SERVER_ERROR) {
	            String redisData = redisTemplate.opsForValue().get(redisKey);
	            if (redisData != null) {
	                JSONParser parser = new JSONParser();
	                JSONObject dataObj = (JSONObject) parser.parse(redisData);
	                return dataObj;
	            }
	        }

	        // If the response code is not 200 OK or 500 Internal Server Error, return an error response
	        JSONObject errorResponse = new JSONObject();
	        errorResponse.put("status", responseEntity.getStatusCodeValue());
	        errorResponse.put("error", responseEntity.getStatusCode().getReasonPhrase());
	        return errorResponse;

	    } catch (ResourceAccessException e) {
	        // Handle the exception by retrieving the latest data from Redis
	        String redisData = redisTemplate.opsForValue().get(redisKey);
	        if (redisData != null) {
	            JSONParser parser = new JSONParser();
	            JSONObject dataObj = (JSONObject) parser.parse(redisData);
	            return dataObj;
	        }

	        // If there is no cached data, return an error response
	        JSONObject errorResponse = new JSONObject();
	        errorResponse.put("status", "Connection Error");
	        errorResponse.put("error", "Error connecting to the server.");
	        return errorResponse;
	    }
	}
	
	@Autowired
    RecommendationService recommendationService;
	
	
	@Value("${twitter.api.url}") 
	private String twitterDetailsUrl;
	@CrossOrigin
	@GetMapping("/getTwitter")
	public JSONObject getTwitterDetails() throws IOException, ParseException {
		RestTemplate restTemplate = new RestTemplate();
	    String response;

	    try {
	        response = restTemplate.getForObject(twitterDetailsUrl, String.class);
	    } catch (HttpClientErrorException e) {
	        // Handle HTTP errors, e.g., 404 Not Found
	        // You can create and return a JSON object with an error message or status code
	        Recommendation recommendation = recommendationService.getLatestRecommendation();
	        JSONObject jsonObject = new JSONObject();
	        jsonObject.put("incident", recommendation.getIncident());
	        jsonObject.put("location", recommendation.getLocation());
	        jsonObject.put("message", recommendation.getMessage());
	        return jsonObject;
	    }

	    JSONParser parse = new JSONParser();
	    JSONObject jsonObject = (JSONObject) parse.parse(response);
	    String incident = (String) jsonObject.get("incident");
	    String location = (String) jsonObject.get("location");
	    String message = (String) jsonObject.get("message");

	    Recommendation recommendation = new Recommendation(incident, location, message);
	    recommendation = recommendationService.createRecommendation(recommendation);
	    return jsonObject;
	}
	
	@Value("${taxi.api.url}")
	private String taxiDetailsUrl;
	@CrossOrigin
	@GetMapping("/getTaxi")
	public JSONObject getTaxiDetails() throws IOException, ParseException {
	    String redisKey = "taxiDetails";
	    JSONObject responseJson = null;

	    try {
	        // Try to make the API call and get the response
	        RestTemplate restTemplate = new RestTemplate();
	        ResponseEntity<String> responseEntity = restTemplate.getForEntity(taxiDetailsUrl, String.class);
	        if (responseEntity.getStatusCode() == HttpStatus.OK) {
	            String response = responseEntity.getBody();
	            responseJson = (JSONObject) new JSONParser().parse(response);

	            // Store the response in Redis
	            template.opsForValue().set(redisKey, response);
	        } else if (responseEntity.getStatusCode() == HttpStatus.INTERNAL_SERVER_ERROR) {
	            // If the API call fails with a 500 error, fetch the latest data from Redis
	            String response = template.opsForValue().get(redisKey);
	            responseJson = (JSONObject) new JSONParser().parse(response);
	        }

	        // If the response code is not 200 OK or 500 Internal Server Error, return an error response
	        if (responseJson == null) {
	            JSONObject errorResponse = new JSONObject();
	            errorResponse.put("status", responseEntity.getStatusCodeValue());
	            errorResponse.put("error", responseEntity.getStatusCode().getReasonPhrase());
	            return errorResponse;
	        }
	    } catch (ResourceAccessException e) {
	        // If the API call fails due to network error, fetch the latest data from Redis
	        String response = template.opsForValue().get(redisKey);
	        if (response != null) {
	            responseJson = (JSONObject) new JSONParser().parse(response);
	        }

	        // If there is no cached data, return an error response
	        if (responseJson == null) {
	            JSONObject errorResponse = new JSONObject();
	            errorResponse.put("status", "Connection Error");
	            errorResponse.put("error", "Error connecting to the server.");
	            return errorResponse;
	        }
	    }

	    return responseJson;
	}
	
	@Value("${bike.api.url}")
	private String bikeDetailsUrl;

	@CrossOrigin
	@GetMapping("/getBike/{id}")
	public JSONObject getBikeDetails(@PathVariable Integer id) throws IOException, ParseException {
	    RestTemplate restTemplate = new RestTemplate();
	    String PREDICTION_URL = "http://10.6.35.134:8080/prediction/" + id;
	    String predictionResponse = restTemplate.getForObject(PREDICTION_URL, String.class);
	    JSONParser predictionParser = new JSONParser();
	    JSONObject predictionObj = (JSONObject) predictionParser.parse(predictionResponse);
	    int prediction = Integer.parseInt(predictionObj.get("prediction").toString());

	    String BIKE_URL = bikeDetailsUrl + id + "?contract=dublin" + "&apiKey=bf3fc6be8642c5b4196db137cadb741e68a4b448";
	    String bikeResponse = restTemplate.getForObject(BIKE_URL, String.class);
	    JSONParser bikeParser = new JSONParser();
	    JSONObject data_obj = (JSONObject) bikeParser.parse(bikeResponse);
	    data_obj.put("prediction", prediction);

	    return data_obj;
	}
	
	
	@Value("${cab.cluster.api.url}")
	private String cabClusterUrl;

	@CrossOrigin
	@PostMapping("/getCabCluster")
	public ResponseEntity<JSONObject> getCabCluster(@RequestBody JSONObject requestBody) {
	    RestTemplate restTemplate = new RestTemplate();
	    HttpHeaders headers = new HttpHeaders();
	    headers.setContentType(MediaType.APPLICATION_JSON);

	    HttpEntity<String> entity = new HttpEntity<>(requestBody.toJSONString(), headers);
	    ResponseEntity<String> responseEntity = restTemplate.exchange(cabClusterUrl, HttpMethod.POST, entity, String.class);

	    if (responseEntity.getStatusCode() == HttpStatus.OK) {
	        String response = responseEntity.getBody();
	        JSONParser parse = new JSONParser();
	        JSONObject cabClusterObj;
	        try {
	            cabClusterObj = (JSONObject) parse.parse(response);
	            JSONObject resultObj = new JSONObject();
	            resultObj.putAll(cabClusterObj);
	            String incident = (String) resultObj.get("incident");
	    	    String location = (String) resultObj.get("location");
	    	    String message = (String) resultObj.get("message");
	    	    Recommendation recommendation = new Recommendation(incident, location, message);
	    	    recommendation = recommendationService.createRecommendation(recommendation);
	            return ResponseEntity.ok(resultObj);
	        } catch (ParseException e) {
	            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
	        }
	    } else {
	        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
	    }
	}

}