#  Risk Awareness Data Pipeline Project

## 📌 About the Project

It's a **risk detection system** for a card system associated with fleet business.

PROBLEM STATEMENT: 

- Pipelines fail due to bad source data even after transformations.
- Costs are incurred even if data is wrong with the pipeline runs 
- Risks are detected too late,only after execution

So in this project, I tried to:

👉 Detect **data issues + transaction risks early**  
👉 Simulate real-world problems like duplicates, nulls, wrong formats  
👉 Build an **end-to-end pipeline + backend + UI**

---

## 🧱 What this project does

1. Generates random realistic datasets  
2. Runs a data pipeline to:
   - Validate data
   - Detect risks
3. Stores output in CSV  
4. Backend (Spring Boot) reads this data  
5. Frontend (React) shows risks in UI  

---


---

## 📊 Datasets Used

### 1. Card Master
- card_id
- driver_id
- vehicle_id
- daily_limit
- card_status (active/blocked)

---

### 2. Transactions
- transaction_id
- card_id
- amount
- timestamp
- location
- merchant_type

---

### 3. PIN Logs
- attempts
- status (success/failed)

---

### 4. Source Errors
- null values
- invalid formats
- duplicates

---

##  Pipeline Steps

### Step 1: Data Validation
Checks:
- NULL values
- Negative amounts
- Invalid timestamps
- Duplicate records

---

### Step 2: Risk Detection

Some risks detected:

- HIGH_AMOUNT  
- PIN_FAILURE  
- BLOCKED_CARD  
- RAPID_TOLL  
- LOCATION_ANOMALY  
- LIMIT_BREACH  

Each transaction gets:
- Risk types  
- Score  
- Priority (LOW / MEDIUM / HIGH)

---

## 🧠 Key Learnings

- Bad data distribution can break risk systems  
- Too many risks → everything becomes HIGH  
- Need to balance data using weights  
- Real-world pipelines fail more due to data than code  

---

## 🛠️ Tech Stack

- Python (Pandas)
- Spring Boot (Java)
- React (Frontend)


---

##  

### 1. Generate Data
### 2. Run pipeline
### 3. Run backend
### 4. Run frontend

