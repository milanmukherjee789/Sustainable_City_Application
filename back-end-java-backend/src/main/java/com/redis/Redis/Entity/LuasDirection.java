package com.redis.Redis.Entity;

import javax.persistence.*;

@Entity
@Table(name = "luas_directions")
public class LuasDirection {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "luas_stop_id", nullable = false)
    private LuasStop luasStop;

    private String destination;
    private String dueMins;
	public Long getId() {
		return id;
	}
	public void setId(Long id) {
		this.id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public LuasStop getLuasStop() {
		return luasStop;
	}
	public void setLuasStop(LuasStop luasStop) {
		this.luasStop = luasStop;
	}
	public String getDestination() {
		return destination;
	}
	public void setDestination(String destination) {
		this.destination = destination;
	}
	public String getDueMins() {
		return dueMins;
	}
	public void setDueMins(String dueMins) {
		this.dueMins = dueMins;
	}
	public LuasDirection(Long id, String name, LuasStop luasStop, String destination, String dueMins) {
		super();
		this.id = id;
		this.name = name;
		this.luasStop = luasStop;
		this.destination = destination;
		this.dueMins = dueMins;
	}
	public LuasDirection() {
		super();
		// TODO Auto-generated constructor stub
	}
}
