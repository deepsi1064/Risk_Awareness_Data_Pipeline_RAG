package com.risk.backend.controller;

import com.risk.backend.model.Risk;
import com.risk.backend.service.RiskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/risk")
@CrossOrigin(origins = "http://localhost:3000")
public class RiskController {

    @Autowired
    private RiskService riskService;
    
    @GetMapping("/all")
    public List<Risk> getAll() {
        return riskService.getAllRisks();
    }

    @GetMapping("/{id}")
    public Risk getById(@PathVariable String id) {
        return riskService.getRiskById(id);
    }
}