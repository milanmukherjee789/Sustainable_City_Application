package com.redis.Redis;

import com.redis.Redis.Controller.RecommendationController;
import com.redis.Redis.Entity.Recommendation;
import com.redis.Redis.Service.RecommendationService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.time.Clock;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

public class RecommendationControllerTest {

    @InjectMocks
    RecommendationController recommendationController;

    @Mock
    RecommendationService recommendationService;

    private Clock clock;
    
    @Autowired
    private MockMvc mockMvc;

    @BeforeEach
    public void setup() {
        MockitoAnnotations.openMocks(this);
        clock = Clock.fixed(Instant.now(), ZoneId.systemDefault());
        mockMvc = MockMvcBuilders.standaloneSetup(recommendationController).build();
    }

    @Test
    public void testCreateRecommendation() {
        Recommendation recommendation = new Recommendation("incident", "location", "message", LocalDateTime.now(clock));
        when(recommendationService.createRecommendation(any(Recommendation.class))).thenReturn(recommendation);
        Recommendation createdRecommendation = recommendationController.createRecommendation(recommendation);
        assertEquals(createdRecommendation, recommendation);
    }

    @Test
    public void testGetAllRecommendations() {
        List<Recommendation> recommendations = Arrays.asList(
                new Recommendation("incident1", "location1", "message1", LocalDateTime.now(clock)),
                new Recommendation("incident2", "location2", "message2", LocalDateTime.now(clock))
        );
        when(recommendationService.getAllRecommendations()).thenReturn(recommendations);
        List<Recommendation> allRecommendations = recommendationController.getAllRecommendations().getBody();
        assertEquals(allRecommendations, recommendations);
    }

    @Test
    public void testGetOneRecommendation() {
        Recommendation recommendation = new Recommendation("incident", "location", "message", LocalDateTime.now(clock));
        when(recommendationService.getOneRecommendation(1)).thenReturn(recommendation);
        Recommendation fetchedRecommendation = recommendationController.getOneRecommendation(1);
        assertEquals(fetchedRecommendation, recommendation);
    }

    @Test
    public void testUpdateRecommendation() {
        Recommendation recommendation = new Recommendation("incident", "location", "message", LocalDateTime.now(clock));
        when(recommendationService.updateRecommendation(any(Recommendation.class), eq(1))).thenReturn(recommendation);
        Recommendation updatedRecommendation = recommendationController.updateRecommendation(recommendation, 1);
        assertEquals(updatedRecommendation, recommendation);
    }

    @Test
    public void testDeleteRecommendation() {
        doNothing().when(recommendationService).deleteRecommendation(1);
        String response = recommendationController.deleteRecommendation(1);
        assertEquals("true", response);
    }

    @Test
    public void testGetNewRecommendations() {
        Recommendation oldRecommendation = new Recommendation("incident1", "location1", "message1", LocalDateTime.now(clock).minusMinutes(5));
        Recommendation newRecommendation = new Recommendation("incident2", "location2", "message2", LocalDateTime.now(clock));
        List<Recommendation> recommendations = Arrays.asList(oldRecommendation, newRecommendation);
        when(recommendationService.getAllRecommendations()).thenReturn(recommendations);
        List<Recommendation> newRecommendations = recommendationController.getNewRecommendations().getBody();
        assertEquals(newRecommendations.size(), 1);
        assertEquals(newRecommendations.get(0), newRecommendation);
    }
    
    @Test
    public void testGetOldRecommendations() throws Exception {
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime twoMinutesAgo = now.minusMinutes(2);
        List<Recommendation> recommendations = Arrays.asList(
            new Recommendation("Incident 1", "Location 1", "Message 1", now),
            new Recommendation("Incident 2", "Location 2", "Message 2", twoMinutesAgo),
            new Recommendation("Incident 3", "Location 3", "Message 3", twoMinutesAgo),
            new Recommendation("Incident 4", "Location 4", "Message 4", now)
        );

        when(recommendationService.getAllRecommendations()).thenReturn(recommendations);

        mockMvc.perform(get("/recommendations/oldrecommendations"))
                .andExpect(status().isOk())
                .andExpect(content().contentType(MediaType.APPLICATION_JSON_VALUE))
                .andExpect(jsonPath("$.length()").value(2))
                .andExpect(jsonPath("$.[0].incident").value("Incident 2"))
                .andExpect(jsonPath("$.[0].location").value("Location 2"))
                .andExpect(jsonPath("$.[0].message").value("Message 2"))
                .andExpect(jsonPath("$.[1].incident").value("Incident 3"))
                .andExpect(jsonPath("$.[1].location").value("Location 3"))
                .andExpect(jsonPath("$.[1].message").value("Message 3"));
    }

}