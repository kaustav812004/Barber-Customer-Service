from crewai import Agent, LLM
from langchain_openai import AzureChatOpenAI
from tools.barber_tools import ALL_TOOLS

from langchain_core.runnables import RunnableLambda

import os
from dotenv import load_dotenv
load_dotenv()

class BarberAgents:
    def __init__(self, model="gpt-4o"):
        try:
            self.llm = LLM(
                api_base=os.getenv("AZURE_API_BASE"),
                api_key=os.getenv("AZURE_API_KEY"),
                api_version=os.getenv("AZURE_API_VERSION"),
                model="azure/gpt-4o",
                temperature=0.7,
                max_tokens=1000,
                timeout=60,
                max_retries=3
            )
            

            print("LLM Ready from crewai.LLM")
        except Exception as e:
            print("[ERROR] Azure LLM init failed:", e)
            raise

    def customer_service_manager(self):
        return Agent(
            role="Customer Service Manager",
            goal="Help customers with appointments, questions, and resolving any issues",
            backstory="You work in a premium barber shop helping customers every day.",
            tools=[t for t in ALL_TOOLS if t.name in [
                "Get Customer Info",
                "Search Knowledge Base",
                "Get Appointment Status",
                "Make Appointment",
                "Check Availability",
                "Get Services and Prices"
            ]],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def appointment_booking_specialist(self):
        return Agent(
            role="Appointment Booking Specialist",
            goal="Schedule appointments and manage booking slots efficiently",
            backstory="You are detail-oriented and know how to fill up a barber's calendar efficiently.",
            tools=[t for t in ALL_TOOLS if t.name in [
                "Check Availability",
                "Make Appointment",
                "Get Appointment Status",
                "Get Customer Info"
            ]],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def service_consultant(self):
        return Agent(
            role="Service Consultant",
            goal="Help customers choose the best grooming service",
            backstory="You know everything about hairstyles and customer grooming.",
            tools=[t for t in ALL_TOOLS if t.name in [
                "Search Knowledge Base",
                "Get Services and Prices",
                "Get Customer Info"
            ]],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def pricing_payment_specialist(self):
        return Agent(
            role="Pricing and Payment Specialist",
            goal="Explain service prices and offers clearly to customers",
            backstory="You ensure pricing is never a confusion for customers.",
            tools=[t for t in ALL_TOOLS if t.name in [
                "Get Services and Prices",
                "Search Knowledge Base",
                "Get Customer Info"
            ]],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def customer_support_agent(self):
        return Agent(
            role="Customer Support Agent",
            goal="Resolve any complaints or service issues with empathy and speed",
            backstory="You are trained in customer retention and problem resolution.",
            tools=[t for t in ALL_TOOLS if t.name in [
                "Get Customer Info",
                "Get Appointment Status",
                "Search Knowledge Base",
                "Make Appointment"
            ]],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
