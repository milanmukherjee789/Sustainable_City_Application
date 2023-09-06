package com.redis.Redis;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

import com.redis.Redis.Service.InvoiceService;
import com.redis.Redis.Service.RecommendationService;

@SpringBootTest
@AutoConfigureMockMvc
@ExtendWith(SpringExtension.class)
public class LuasControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private RestTemplate restTemplate;

    @MockBean
    private ValueOperations<String, String> valueOperations;

    @MockBean
    private StringRedisTemplate stringRedisTemplate;
  

    private String stop = "MUS";
    private String luasApiUrl = "http://10.6.39.91:8000/luas/stop/";
    private String luasRedisKeyPrefix = "luas_";
    private String redisKey = luasRedisKeyPrefix + stop;

    private String luasResponse;

    @BeforeEach
    public void setUp() throws IOException {
        when(stringRedisTemplate.opsForValue()).thenReturn(valueOperations);
        luasResponse = readResourceFileAsString("luas_response.json");
    }

    private String readResourceFileAsString(String fileName) throws IOException {
        Path path = Paths.get("src", "test", "resources", fileName);
        byte[] bytes = Files.readAllBytes(path);
        return new String(bytes, StandardCharsets.UTF_8);
    }

    @Test
    public void testGetLuasDetails_success() throws Exception {
        ResponseEntity<String> responseEntity = new ResponseEntity<>(luasResponse, HttpStatus.OK);

        when(restTemplate.getForEntity(luasApiUrl + stop, String.class)).thenReturn(responseEntity);
        mockMvc.perform(get("/request/luas/stop/{stop}", stop))
                .andExpect(status().isOk());
    }

    @Test
    public void testGetLuasDetails_internalServerError() throws Exception {
        ResponseEntity<String> responseEntity = new ResponseEntity<>(luasResponse, HttpStatus.INTERNAL_SERVER_ERROR);

        when(restTemplate.getForEntity(luasApiUrl + stop, String.class)).thenReturn(responseEntity);
        when(valueOperations.get(redisKey)).thenReturn(luasResponse);

        mockMvc.perform(get("/request/luas/stop/{stop}", stop))
                .andExpect(status().isOk());
    }

    @Test
    public void testGetLuasDetails_connectionError() throws Exception {
        String responseBody = "{\"status\":\"Connection Error\",\"error\":\"Error connecting to the server.\"}";

        when(restTemplate.getForEntity(luasApiUrl + stop, String.class)).thenThrow(ResourceAccessException.class);
        when(valueOperations.get(redisKey)).thenReturn(null);

        mockMvc.perform(get("/request/luas/stop/{stop}", stop))
                .andExpect(status().isOk());
    }

    @Test
    public void testGetLuasDetails_otherError() throws Exception {
        String responseBody = "{\"status\":404,\"error\":\"Not Found\"}";
        ResponseEntity<String> responseEntity = new ResponseEntity<>(responseBody, HttpStatus.NOT_FOUND);

        when(restTemplate.getForEntity(luasApiUrl + stop, String.class)).thenReturn(responseEntity);
        mockMvc.perform(get("/request/luas/stop/{stop}", stop))
                .andExpect(status().isOk());
    }
}
