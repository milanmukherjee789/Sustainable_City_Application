package com.redis.Redis.Repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.redis.Redis.Entity.LuasStop;

@Repository
public interface LuasStopRepository extends JpaRepository<LuasStop, Long> {
	LuasStop findByStopAbv(String stopAbv);
}
