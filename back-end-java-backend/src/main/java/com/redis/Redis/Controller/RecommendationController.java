package com.redis.Redis.Controller;
import org.springframework.beans.factory.annotation.Autowired;
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

import com.redis.Redis.Entity.Recommendation;
import com.redis.Redis.Service.RecommendationService;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/recommendations")
public class RecommendationController {

    @Autowired
    RecommendationService recommendationService;

    @CrossOrigin
    @PostMapping("/create")
    public Recommendation createRecommendation(@RequestBody Recommendation recommendation) {
        return recommendationService.createRecommendation(recommendation);
    }

    @CrossOrigin
    @GetMapping("/all")
    public ResponseEntity<List<Recommendation>> getAllRecommendations() {
        return ResponseEntity.ok(recommendationService.getAllRecommendations());
    }

    @CrossOrigin
    @GetMapping("/get/{id}")
    public Recommendation getOneRecommendation(@PathVariable Integer id) {
        return recommendationService.getOneRecommendation(id);
    }

    @CrossOrigin
    @PutMapping("/update/{id}")
    public Recommendation updateRecommendation(@RequestBody Recommendation recommendation, @PathVariable Integer id) {
        return recommendationService.updateRecommendation(recommendation, id);
    }

    @CrossOrigin
    @DeleteMapping("/delete/{id}")
    public String deleteRecommendation(@PathVariable Integer id) {
        recommendationService.deleteRecommendation(id);
        return "true";
    }
    
    @CrossOrigin
    @GetMapping("/newrecommendations")
    public ResponseEntity<List<Recommendation>> getNewRecommendations() {
        LocalDateTime twoMinutesAgo = LocalDateTime.now().minusMinutes(2);
        List<Recommendation> newRecommendations = recommendationService.getAllRecommendations()
                .stream()
                .filter(recommendation -> recommendation.getTimestamp().isAfter(twoMinutesAgo))
                .collect(Collectors.toList());
        return ResponseEntity.ok(newRecommendations);
    }

    @CrossOrigin
    @GetMapping("/oldrecommendations")
    public ResponseEntity<List<Recommendation>> getOldRecommendations() {
        LocalDateTime twoMinutesAgo = LocalDateTime.now().minusMinutes(2);
        List<Recommendation> oldRecommendations = recommendationService.getAllRecommendations()
                .stream()
                .filter(recommendation -> recommendation.getTimestamp().isBefore(twoMinutesAgo))
                .collect(Collectors.toList());
        return ResponseEntity.ok(oldRecommendations);
    }
}
