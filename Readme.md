# ♻️ CivicBio  
### Biomedical Waste Management System for Civic Bodies

CivicBio is a **role-based, QR-enabled biomedical waste management platform** designed to help civic authorities monitor, regulate, and audit the complete lifecycle of biomedical waste — from **generation at healthcare facilities** to **collection and final disposal**.

The system focuses on **accountability, traceability, and compliance**, aligned with India’s **Biomedical Waste Management Rules**.

---

## 🚀 Problem Statement

Biomedical waste mismanagement leads to:
- Public health risks  
- Environmental contamination  
- Lack of traceability and accountability  
- Manual, paper-based compliance  

Existing systems lack **real-time visibility**, **digital verification**, and **role-based control**.

---

## 💡 Solution Overview

CivicBio introduces a **digitally traceable workflow** using:
- Role-based dashboards  
- QR code–based waste tracking  
- Civic approval & profile locking  
- Real-time KPIs and audit trails  

Every waste batch is **digitally verifiable** at each stage.

---

## 👥 Actors & Roles

### 🏥 Facility (Hospitals / Labs / Clinics)
- Register and set up facility profile  
- Generate biomedical waste batches  
- Print & paste QR codes on waste bags  
- Track pickup and disposal status  
- View compliance status  

### 🚛 Collector
- Verify facility via QR scan  
- Scan waste batch QR to mark as collected  
- Upload pickup proof  
- Report issues  
- Hand over waste to disposal unit  

### ♻️ Disposal Unit (CBWTF / Incinerator)
- Scan waste QR to verify eligibility  
- Select disposal method  
- Mark waste as disposed  
- View daily KPIs  

### 🏛️ Civic Authority
- Approve / reject profiles  
- View city-wide KPIs  
- Monitor waste lifecycle  
- Track reported issues  

---

## 🔁 Waste Lifecycle

Facility → QR Generation → Collection → Disposal → Civic Audit

---

## 🧱 Tech Stack

**Backend:** Python, Flask, MongoDB (MongoEngine)  
**Frontend:** HTML, CSS, JavaScript, Bootstrap, jQuery  
**Storage:** Supabase  
**Other:** QR Codes, jsQR, IST timezone handling  

---

## 🔐 Key Features

- Profile lock until civic approval  
- QR-based verification at every stage  
- Role-based dashboards  
- Real-time KPIs  
- Issue reporting & audit trail  

---

## 📂 Project Structure

app/  
├── routes/  
├── models/  
├── templates/  
├── static/  
└── extensions/  

---

## 🎯 Hackathon Focus

CivicBio is designed as a **governance-first prototype**, emphasizing real-world applicability, regulatory compliance, and traceability.

---
