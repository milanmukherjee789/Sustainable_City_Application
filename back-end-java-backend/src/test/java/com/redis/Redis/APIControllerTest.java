/*

package com.redis.Redis;
import com.redis.Redis.Controller.InvoiceController;
import com.redis.Redis.Entity.Invoice;
import com.redis.Redis.Service.InvoiceService;
import com.redis.Redis.Service.RecommendationService;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import org.junit.runner.RunWith;
import org.mockito.MockitoAnnotations;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.redis.core.StringRedisTemplate;

import org.springframework.test.context.junit4.SpringRunner;

import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;




import static org.junit.Assert.*;


import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneId;

import static org.mockito.ArgumentMatchers.anyString;

@RunWith(SpringRunner.class)
@WebMvcTest(InvoiceController.class)
public class APIControllerTest {

	
	@Autowired
    private InvoiceController invoiceController;

    private MockMvc mockMvc;
    
    @MockBean
    private StringRedisTemplate stringRedisTemplate;
    
    @MockBean
    private InvoiceService invoiceService;
    
    @MockBean
    private RecommendationService recommendationService;
    
    @BeforeEach
    public void setup() {
        //MockitoAnnotations.openMocks(this);
        this.mockMvc = MockMvcBuilders.standaloneSetup(invoiceController).build();
    }
    
    @AfterEach
    public void tearDown() throws Exception {
        mockMvc.perform(MockMvcRequestBuilders.post("/shutdown"));
    }

    
	  private String readJsonFromFile(String filePath) throws IOException { 
	  Path path = Paths.get(filePath); byte[] bytes = Files.readAllBytes(path); return
	  new String(bytes, StandardCharsets.UTF_8); }
	 
    
	  @Test
	  public void testGetBusDetails() throws Exception {
	      String jsonContent = readJsonFromFile("src/test/resources/bus_response.json");
	      JSONParser parser = new JSONParser();
	      JSONObject dataObj = (JSONObject) parser.parse(jsonContent);

	      given(invoiceController.getBusDetails(anyString())).willReturn(dataObj);

	      MvcResult result = mockMvc.perform(get("request/bus/stop/{busNumber}", "1474"))
	              .andExpect(status().isOk())
	              .andReturn();

	      String jsonResponse = result.getResponse().getContentAsString();
	      JSONObject responseObj = (JSONObject) parser.parse(jsonResponse);

	      assertEquals(dataObj, responseObj);
	  }

	  
	
}
*/