# tools/barber_tools.py
from langchain_core.tools import tool

@tool
def get_customer_info(name: str) -> str:
    """Fetch customer record using name"""
    return f"Customer record fetched for {name}."

@tool
def search_knowledge_base(query: str) -> str:
    """Search for common barber service questions"""
    return f"Knowledge base response for query: '{query}'"

@tool
def get_appointment_status(customer_id: str) -> str:
    """Check a customer's appointment status"""
    return f"Appointment status for customer {customer_id}: Confirmed."

@tool
def make_appointment(date: str, time: str, service: str) -> str:
    """Book an appointment with date, time and service"""
    return f"Appointment booked for {service} on {date} at {time}."

@tool
def check_availability(date: str, time: str) -> str:
    """Check if a slot is available at a given time and date"""
    return f"Availability checked for {date} at {time}: Slot available."

@tool
def get_services_and_prices() -> dict:
    """List all available services and their prices"""
    return {
        "Haircut": "$25",
        "Beard Trim": "$15",
        "Haircut + Beard": "$35",
        "Premium Grooming Package": "$60"
    }

ALL_TOOLS = [
    get_customer_info,
    search_knowledge_base,
    get_appointment_status,
    make_appointment,
    check_availability,
    get_services_and_prices
]
