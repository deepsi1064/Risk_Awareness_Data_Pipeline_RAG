package com.risk.backend.service;

import com.risk.backend.model.Risk;
import org.springframework.stereotype.Service;

import java.io.*;
import java.util.*;

@Service
public class RiskService {

    private static final String FILE_PATH =
            "C:/Users/deeps/OneDrive/Documents/Risk-Awareness_Data_Pipeline_for_source/data/processed/risk_output.csv";

    public List<Risk> getAllRisks() {

        List<Risk> risks = new ArrayList<>();

        System.out.println("==== START READING FILE ====");
        System.out.println("Path: " + FILE_PATH);

        try (BufferedReader br = new BufferedReader(new FileReader(FILE_PATH))) {

            String line;

            // skip header
            br.readLine();

            while ((line = br.readLine()) != null) {

                System.out.println("LINE => " + line);

                // 🔥 CUSTOM CSV PARSER (handles quotes correctly)
                List<String> parts = new ArrayList<>();
                boolean inQuotes = false;
                StringBuilder current = new StringBuilder();

                for (char c : line.toCharArray()) {
                    if (c == '"') {
                        inQuotes = !inQuotes;
                    } else if (c == ',' && !inQuotes) {
                        parts.add(current.toString());
                        current.setLength(0);
                    } else {
                        current.append(c);
                    }
                }
                parts.add(current.toString());

                // safety check
                if (parts.size() < 4) {
                    System.out.println("Skipping bad row");
                    continue;
                }

                try {
                    String transactionId = parts.get(0);
                    String risksStr = parts.get(1);
                    int score = Integer.parseInt(parts.get(2));
                    String priority = parts.get(3);

                    risks.add(new Risk(transactionId, risksStr, score, priority));

                } catch (Exception e) {
                    System.out.println("Error parsing row: " + line);
                    e.printStackTrace();
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.println("TOTAL RISKS: " + risks.size());

        return risks;
    }

    public Risk getRiskById(String txnId) {
        return getAllRisks().stream()
                .filter(r -> r.getTransactionId().equals(txnId))
                .findFirst()
                .orElse(null);
    }
}