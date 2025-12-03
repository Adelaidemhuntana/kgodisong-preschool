

# 🌟 Kgodisong Preschool – Child Health & Wellness AI Assistant

**Hackathon Project – Health Innovation**

## 🧒🏽💙 Overview

This project integrates **Meta Llama AI** into a preschool website to create a **Child Health & Wellness Assistant** for parents and teachers.
It helps with:

* Booking **immunizations & vaccines**
* Booking **eye tests** & **dental checkups**
* Logging children’s **sick absences**
* Giving **safe first-aid guidance** while waiting for medical help
* Providing **nutrition, behaviour & development advice**

The goal is to support schools and parents and reduce missed vaccinations for children.

---

## 🎯 Problem We’re Solving

Parents struggle with:

* Taking time off work for clinic visits
* Kids missing vaccines or checkups
* Not knowing what to do when a child suddenly gets sick
* No quick guidance while waiting for an ambulance
* Schools having no digital way to log health-related absences

**Kgodisong Preschool + AI = Accessible health support for every parent.**

---

## 🧠 Solution Summary

We add a new page to the Kgodisong Preschool website:

### **📌 Child Health & Wellness AI Page**

Includes:

* A textbox (user question)
* A dropdown:

  * Symptoms
  * Nutrition
  * Behaviour
  * Development
* Booking forms for:

  * Immunizations & vaccines
  * Eye test
  * Dental check
* Sick-absence logging
* Safe guidance using **Llama 3.1**

---

## 🧩 Tech Stack

* **HTML / CSS / JavaScript** (frontend)
* **Meta Llama API (Tools via Llama Cookbook)**
* **Optional Backend:** Node.js or Flask
* **Database:** Firebase / Supabase / MySQL (for booking data)

---

## 🔌 Llama Tools Used

### **1. Tool: Llama Text Generation**

* For symptoms, nutrition, development, behaviour guidance
* Provides safe, simple explanations
* Includes safety rules (No diagnosis)

### **2. Tool: RAG (Retrieval-Augmented Generation)**

* For:

  * Immunization schedules
  * School health policies
  * First-aid instructions
* Stores school-specific documents

### **3. Tool: Structured Outputs**

* For clean responses like:

  * `"risk_level": "low"`
  * `"next_steps": "Give warm water, observe child"`
* Makes the system safe and predictable

### **4. Tool: Function Calling**

* For:

  * Creating bookings
  * Logging a child sick
  * Fetching immunization dates

---

## 🛠️ Setup Instructions (Simple)

1. Clone the repo
2. Install dependencies
3. Add your Meta Llama API key to `.env`
4. Run the backend (Node/Flask)
5. Open the website in browser

---

## 🚀 How It Works

### **1. Parent selects a category**

Example: “Symptoms”

### **2. Parent types a concern**

Example: “My child has a fever and is vomiting”

### **3. Llama returns safe steps**

* Drink fluids
* Keep child cool
* Warning signs
* When to call clinic/ambulance

### **4. Parent can book**

* Vaccine date
* Eye test
* Dental checkup

### **5. School can log absences**

---

## 🧪 Example Llama Prompt

```json
{
  "category": "symptoms",
  "child_age": "4",
  "question": "My child has a fever and is vomiting. What should I do while waiting for an ambulance?",
  "safety_rules": "No diagnosis. Give immediate safety steps only."
}
```

---

## 📅 Partnership Model

Kgodisong Preschool partners with:

* Local government clinics
* Mobile health teams
* NGO child wellness programs

They visit **monthly** for:

* Vaccines
* Health screening
* Eye and dental checks

---

## 👩🏽‍💻 Developer: Adelaide Mhuntana

Hackathon: **Health Innovation Challenge**
Team Name: **AI Health Builders** (or any you choose)

---

## ✔️ Status

⏳ Version 1: Basic Llama integration
🚧 Next: Add booking backend and notifications


