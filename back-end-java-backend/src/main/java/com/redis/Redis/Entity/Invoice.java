package com.redis.Redis.Entity;

import java.io.Serializable;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

import lombok.Data;

@Data
@Entity
public class Invoice implements Serializable{

   private static final long serialVersionUID = -4439114469417994311L;

   @Id
   @GeneratedValue
   private Integer invId;
   //private String invName;
   //private Double invAmount;
   private String userName;
   private String passWord;
public Integer getInvId() {
	return invId;
}
public void setInvId(Integer invId) {
	this.invId = invId;
}
public String getUserName() {
	return userName;
}
public void setUserName(String userName) {
	this.userName = userName;
}
public String getPassWord() {
	return passWord;
}
public void setPassWord(String passWord) {
	this.passWord = passWord;
}
public Invoice(Integer invId, String userName, String passWord) {
	super();
	this.invId = invId;
	this.userName = userName;
	this.passWord = passWord;
}
public Invoice() {
	super();
}
}