package com.redis.Redis;
import com.redis.Redis.Controller.InvoiceController;
import com.redis.Redis.Entity.Invoice;
import com.redis.Redis.Service.InvoiceService;
import com.redis.Redis.Service.RecommendationService;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.mock.mockito.SpyBean;
import org.springframework.context.annotation.Import;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.context.WebApplicationContext;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Arrays;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.lenient;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import org.springframework.test.web.servlet.MvcResult;
import org.json.JSONObject;
import static org.junit.Assert.*;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(SpringExtension.class)
@ExtendWith(MockitoExtension.class)
@WebMvcTest(InvoiceController.class)
public class InvoiceControllerTest {

    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private StringRedisTemplate stringRedisTemplate;

    @MockBean
    private InvoiceService invoiceService;

    private Invoice testInvoice;
    private List<Invoice> testInvoiceList;

    @Autowired
    private WebApplicationContext webApplicationContext;
    @MockBean
    private RecommendationService recommendationService;
    
    @BeforeEach
    public void setUp() {
        testInvoice = new Invoice(1, "testUser", "testPass");
        testInvoiceList = Arrays.asList(testInvoice);
        mockMvc = MockMvcBuilders.webAppContextSetup(webApplicationContext).build();
    }

    @Test
    public void testSaveInvoice() throws Exception {
        when(invoiceService.saveInvoice(any(Invoice.class))).thenReturn(testInvoice);

        mockMvc.perform(post("/request/saveUser")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"invId\":1,\"userName\":\"testUser\",\"passWord\":\"testPass\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.invId").value(1))
                .andExpect(jsonPath("$.userName").value("testUser"))
                .andExpect(jsonPath("$.passWord").value("testPass"));
    }

    @Test
    public void testGetAllInvoices() throws Exception {
        when(invoiceService.getAllInvoices()).thenReturn(testInvoiceList);

        mockMvc.perform(get("/request/allUsers"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.[0].invId").value(1))
                .andExpect(jsonPath("$.[0].userName").value("testUser"))
                .andExpect(jsonPath("$.[0].passWord").value("testPass"));
    }

    @Test
    public void testGetOneInvoice() throws Exception {
        when(invoiceService.getOneInvoice(1)).thenReturn(testInvoice);

        mockMvc.perform(get("/request/getOne/{id}", 1))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.invId").value(1))
                .andExpect(jsonPath("$.userName").value("testUser"))
                .andExpect(jsonPath("$.passWord").value("testPass"));
    }
    
    @Test
    public void testGetOneInvoiceBySearchUser() throws Exception {
    	when(invoiceService.getOneInvoice(1)).thenReturn(testInvoice);

        mockMvc.perform(get("/request/getOne/{id}", 1))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.passWord").value("testPass"));
    }

    @Test
    public void testUpdateInvoice() throws Exception {
        Invoice updatedInvoice = new Invoice(1, "updatedUser", "updatedPass");
        when(invoiceService.updateInvoice(any(Invoice.class), any(Integer.class))).thenReturn(updatedInvoice);

        mockMvc.perform(put("/request/modify/{id}", 1)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"invId\":1,\"userName\":\"updatedUser\",\"passWord\":\"updatedPass\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.invId").value(1))
                .andExpect(jsonPath("$.userName").value("updatedUser"))
                .andExpect(jsonPath("$.passWord").value("updatedPass"));
    }

    @Test
    public void testDeleteInvoice() throws Exception {
        mockMvc.perform(delete("/request/delete/{id}", 1))
                .andExpect(status().isOk())
                .andExpect(content().string("User with id: 1 Deleted !"));
    }
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Test
    public void testAuthenticateUser() throws Exception {
        Invoice user1 = new Invoice(1, "user1", "password1");
        Invoice user2 = new Invoice(2, "user2", "password2");

        when(invoiceService.getAllInvoices()).thenReturn(Arrays.asList(user1, user2));

        Invoice validUser = new Invoice(null, "user1", "password1");
        String validUserJson = new ObjectMapper().writeValueAsString(validUser);

        MvcResult result = mockMvc.perform(post("/request/authenticate")
                .contentType(MediaType.APPLICATION_JSON)
                .content(validUserJson))
                .andExpect(status().isOk())
                .andReturn();

        String jsonResponse = result.getResponse().getContentAsString();
        JSONObject jsonObject = new JSONObject(jsonResponse);

        assertTrue(jsonObject.getBoolean("authorized"));
        assertNotNull(jsonObject.getString("token"));

        Invoice invalidUser = new Invoice(null, "invalid", "invalid");
        String invalidUserJson = new ObjectMapper().writeValueAsString(invalidUser);

        MvcResult invalidResult = mockMvc.perform(post("/request/authenticate")
                .contentType(MediaType.APPLICATION_JSON)
                .content(invalidUserJson))
                .andExpect(status().isOk())
                .andReturn();

        String invalidJsonResponse = invalidResult.getResponse().getContentAsString();
        JSONObject invalidJsonObject = new JSONObject(invalidJsonResponse);

        assertFalse(invalidJsonObject.getBoolean("authorized"));
        assertTrue(invalidJsonObject.getString("token").isEmpty());
    }

}
