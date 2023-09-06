package com.redis.Redis.Entity;

import java.time.LocalDateTime;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "recommendations")
public class Recommendation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "incident")
    private String incident;

    @Column(name = "location")
    private String location;

    @Column(name = "message")
    private String message;
    
    @Column(name = "timestamp")
    private LocalDateTime timestamp;

    public Recommendation() {
    }

    public Recommendation(String incident, String location, String message) {
        this.incident = incident;
        this.location = location;
        this.message = message;
        this.timestamp = LocalDateTime.now();
    }
    
    public Recommendation(String incident, String location, String message, LocalDateTime timestamp) {
        this.incident = incident;
        this.location = location;
        this.message = message;
        this.timestamp = timestamp;
    }
    
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getIncident() {
        return incident;
    }

    public void setIncident(String incident) {
        this.incident = incident;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
    
    public LocalDateTime getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(LocalDateTime timestamp) {
        this.timestamp = timestamp;
    }
    
}
