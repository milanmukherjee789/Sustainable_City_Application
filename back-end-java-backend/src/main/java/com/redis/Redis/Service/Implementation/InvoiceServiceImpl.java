package com.redis.Redis.Service.Implementation;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import com.redis.Redis.InvoiceNotFoundException;
import com.redis.Redis.Entity.Invoice;
import com.redis.Redis.Repository.InvoiceRepository;
import com.redis.Redis.Service.InvoiceService;

@Service
public class InvoiceServiceImpl implements InvoiceService {

	@Autowired
	private InvoiceRepository invoiceRepo;

	@Override
	public Invoice saveInvoice(Invoice inv) {

		return invoiceRepo.save(inv);
	}

	@Override
	@CachePut(value = "Invoice", key = "#invId")
	public Invoice updateInvoice(Invoice inv, Integer invId) {
		Invoice invoice = invoiceRepo.findById(invId)
				.orElseThrow(() -> new InvoiceNotFoundException("Invoice Not Found"));
		invoice.setUserName(inv.getUserName());
		invoice.setPassWord(inv.getPassWord());
		return invoiceRepo.save(invoice);
	}

	@Override
	@CacheEvict(value = "Invoice", key = "#invId")
	// @CacheEvict(value="Invoice", allEntries=true) //in case there are multiple
	// entires to delete
	public void deleteInvoice(Integer invId) {
		Invoice invoice = invoiceRepo.findById(invId)
				.orElseThrow(() -> new InvoiceNotFoundException("Invoice Not Found"));
		invoiceRepo.delete(invoice);
	}

	@Override
	@Cacheable(value = "Invoice", key = "#invId")
	public Invoice getOneInvoice(Integer invId) {
		Invoice invoice = invoiceRepo.findById(invId)
				.orElseThrow(() -> new InvoiceNotFoundException("Invoice Not Found"));
		return invoice;
	}

	@Override
	public List<Invoice> getAllInvoices() {
		return invoiceRepo.findAll();
	}

}