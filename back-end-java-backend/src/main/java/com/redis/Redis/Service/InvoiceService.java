package com.redis.Redis.Service;

import java.util.List;

import com.redis.Redis.Entity.Invoice;

public interface InvoiceService {

	public Invoice saveInvoice(Invoice inv);

	public Invoice updateInvoice(Invoice inv, Integer invId);

	public void deleteInvoice(Integer invId);

	public Invoice getOneInvoice(Integer invId);

	public List<Invoice> getAllInvoices();
}