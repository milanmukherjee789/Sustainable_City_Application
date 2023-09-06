package com.redis.Redis.Entity;

import javax.persistence.*;
import java.util.Date;
import java.util.List;

@Entity
@Table(name = "luas_stops")
public class LuasStop {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String stop;
    private Date created;
    private String message;
    private String stopAbv;

    @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "luas_stop_id")
    private List<LuasDirection> direction;

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getStop() {
		return stop;
	}

	public void setStop(String stop) {
		this.stop = stop;
	}

	public Date getCreated() {
		return created;
	}

	public void setCreated(Date created) {
		this.created = created;
	}

	public String getMessage() {
		return message;
	}

	public void setMessage(String message) {
		this.message = message;
	}

	public String getStopAbv() {
		return stopAbv;
	}

	public void setStopAbv(String stopAbv) {
		this.stopAbv = stopAbv;
	}

	public List<LuasDirection> getDirection() {
		return direction;
	}

	public void setDirection(List<LuasDirection> direction) {
		this.direction = direction;
	}

	public LuasStop(Long id, String stop, Date created, String message, String stopAbv, List<LuasDirection> direction) {
		super();
		this.id = id;
		this.stop = stop;
		this.created = created;
		this.message = message;
		this.stopAbv = stopAbv;
		this.direction = direction;
	}

	public LuasStop() {
		super();
		// TODO Auto-generated constructor stub
	}

    
}
