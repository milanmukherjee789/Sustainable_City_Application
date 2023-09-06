package com.redis.Redis;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

import java.io.IOException;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.ParseException;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import com.redis.Redis.Controller.InvoiceController;

@SpringBootTest
class RedisApplicationTests extends InvoiceController {

	@Test
	void contextLoads() {
	}
	
	/*
	 * @Test public void getLuas() throws IOException, ParseException { String stop
	 * = "ran"; JSONObject test = getLuasDetails(stop); assertNotNull(test); }
	 */
}

