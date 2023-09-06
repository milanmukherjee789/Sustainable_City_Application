package com.redis.Redis.Service.Implementation;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.redis.Redis.Entity.Recommendation;
import com.redis.Redis.Repository.RecommendationRepository;
import com.redis.Redis.Service.RecommendationService;


@Service
public class RecommendationServiceImpl implements RecommendationService {

    @Autowired
    RecommendationRepository recommendationRepository;

    @Override
    public Recommendation createRecommendation(Recommendation recommendation) {
    	recommendation.setTimestamp(LocalDateTime.now());
        return recommendationRepository.save(recommendation);
    }

    @Override
    public Recommendation updateRecommendation(Recommendation recommendation, Integer recommendationId) {
        Optional<Recommendation> existingRecommendation = recommendationRepository.findById(recommendationId);
        if (existingRecommendation.isPresent()) {
            Recommendation updatedRecommendation = existingRecommendation.get();
            updatedRecommendation.setIncident(recommendation.getIncident());
            updatedRecommendation.setLocation(recommendation.getLocation());
            updatedRecommendation.setMessage(recommendation.getMessage());
            return recommendationRepository.save(updatedRecommendation);
        } else {
            throw new RuntimeException("Recommendation not found with id: " + recommendationId);
        }
    }

    @Override
    public void deleteRecommendation(Integer recommendationId) {
        recommendationRepository.deleteById(recommendationId);
    }

    @Override
    public Recommendation getOneRecommendation(Integer recommendationId) {
        Optional<Recommendation> recommendation = recommendationRepository.findById(recommendationId);
        if (recommendation.isPresent()) {
            return recommendation.get();
        } else {
            throw new RuntimeException("Recommendation not found with id: " + recommendationId);
        }
    }

    @Override
    public List<Recommendation> getAllRecommendations() {
        return recommendationRepository.findAll();
    }
    
    @Override
    public Recommendation getLatestRecommendation() {
        List<Recommendation> recommendations = recommendationRepository.findAllByOrderByTimestampDesc();
        if (recommendations.isEmpty()) {
            throw new RuntimeException("No recommendations found in the database.");
        } else {
            return recommendations.get(0);
        }
    }
    
}
