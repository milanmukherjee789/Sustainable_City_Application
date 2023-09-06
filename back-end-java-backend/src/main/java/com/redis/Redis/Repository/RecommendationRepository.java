package com.redis.Redis.Repository;


import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.redis.Redis.Entity.Recommendation;


@Repository
public interface RecommendationRepository extends JpaRepository<Recommendation, Integer> {
	List<Recommendation> findAllByOrderByTimestampDesc();
}
