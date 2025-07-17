# 💈 Barber Customer Service Agentic App (CrewAI)

This project simulates a smart, conversational customer service system for a barber shop using **CrewAI**, **LangChain**, and **Azure OpenAI (GPT-4o)**. It automates tasks like booking appointments, recommending services, answering pricing questions, and resolving customer complaints through intelligent agents.

---

## 🚀 Features

* 🤖 Modular AI agents powered by `crewai.Agent`
* 📋 Task-based logic routes requests dynamically
* 🔧 LangChain tools with `@tool` decorators
* 🔐 Secure Azure OpenAI integration (`gpt-4o`)
* 🧪 Supports both CLI-based interaction and scripted examples

---

## 🧠 Agents Overview

| Agent Role                     | Responsibilities                       |
| ------------------------------ | -------------------------------------- |
| Customer Service Manager       | General inquiries, shop info           |
| Appointment Booking Specialist | Bookings, availability, calendar mgmt  |
| Service Consultant             | Personalized service suggestions       |
| Pricing & Payment Specialist   | Pricing, discounts, memberships        |
| Customer Support Agent         | Handles complaints and customer issues |

---

## 📁 Project Structure

```
barber_customer_service/
├── .env                      # Azure credentials
├── main.py                   # App entry point
├── agents.py                 # CrewAI agents setup
├── tasks.py                  # Task templates and logic
├── tools/
│   └── barber_tools.py       # LangChain tools wrapped with @tool
├── requirements.txt          # Python dependencies
└── README.md                 # You're here!
```

---

## 🔐 .env File Configuration

Create a `.env` file with the following variables:

```env
AZURE_API_KEY=your_azure_key
AZURE_API_BASE=https://your-resource-name.openai.azure.com/
AZURE_API_VERSION=2024-02-15-preview
AZURE_DEPLOYMENT_NAME=gpt-4o
```

---

## 💻 Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/barber_customer_service.git
cd barber_customer_service
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Add your `.env` file**

---

## 🧪 Run Examples

```bash
python main.py example
```

This demonstrates common use-cases like appointment booking, pricing inquiries, and service recommendations.

---

## 💬 Run Interactive Mode

```bash
python main.py
```

You'll be guided through a natural conversation to help with bookings, prices, or support.

---

## 🔧 LangChain Tools Used

Defined in `barber_tools.py` using `@tool`:

* `get_customer_info(name)`
* `check_availability(date, time)`
* `make_appointment(date, time, service)`
* `get_services_and_prices()`
* `search_knowledge_base(query)`
* `get_appointment_status(customer_id)`

These tools are assigned to agents depending on their responsibilities.

---

## 📦 Requirements

```
crewai
langchain
langchain-openai
langchain-core
python-dotenv
```

---

## 🤖 Built With

* [CrewAI](https://docs.crewai.com/)
* [LangChain](https://docs.langchain.com/)
* [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/)

---

## 📬 Contributing

Feel free to fork the repo, add your improvements, and open a pull request!

---

