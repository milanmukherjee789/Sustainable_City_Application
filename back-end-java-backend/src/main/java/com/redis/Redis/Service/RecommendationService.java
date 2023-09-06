package com.redis.Redis.Service;


import java.util.List;

import com.redis.Redis.Entity.Recommendation;


public interface RecommendationService {

    public Recommendation createRecommendation(Recommendation recommendation);

    public Recommendation updateRecommendation(Recommendation recommendation, Integer recommendationId);

    public void deleteRecommendation(Integer recommendationId);

    public Recommendation getOneRecommendation(Integer recommendationId);

    public List<Recommendation> getAllRecommendations();

    public Recommendation getLatestRecommendation();
    
}
