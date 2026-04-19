package com.risk.backend.model;

public class Risk {

    private String transactionId;
    private String risks;
    private int score;
    private String priority;

    public Risk(String transactionId, String risks, int score, String priority) {
        this.transactionId = transactionId;
        this.risks = risks;
        this.score = score;
        this.priority = priority;
    }

    public String getTransactionId() { return transactionId; }
    public String getRisks() { return risks; }
    public int getScore() { return score; }
    public String getPriority() { return priority; }
}