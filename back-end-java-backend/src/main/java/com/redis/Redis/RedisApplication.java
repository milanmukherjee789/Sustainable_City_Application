package com.redis.Redis;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.cache.annotation.EnableCaching;
import com.redis.Redis.Util.*;

@SpringBootApplication()
@EnableCaching
public class RedisApplication {

	public static void main(String[] args) {
		SpringApplication.run(RedisApplication.class, args);
	}
	public FilterRegistrationBean<JwtRequestFilter> jwtRequestFilter() {
	    FilterRegistrationBean<JwtRequestFilter> registrationBean = new FilterRegistrationBean<>();
	    registrationBean.setFilter(new JwtRequestFilter());
	    registrationBean.addUrlPatterns("/recommendations/*", "/request/*");
	    return registrationBean;
	}
}
