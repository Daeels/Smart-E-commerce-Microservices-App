package org.sid.lightecomv1.dao;

import org.sid.lightecomv1.entities.Order;
import org.sid.lightecomv1.entities.Payment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;
import org.springframework.web.bind.annotation.CrossOrigin;

@CrossOrigin("*")
@RepositoryRestResource
public interface PayementRepository extends JpaRepository<Payment, Long> {

}
