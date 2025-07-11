from crewai.tools import tool
from dotenv import load_dotenv
import os

# Mock database for demonstration

# Load environment variables
load_dotenv()


# Mock database for demonstration
CUSTOMERS_DB = {
    "john_smith": {
        "name": "John Smith",
        "phone": "555-0123",
        "email": "john@email.com",
        "hair_type": "thick",
        "preferred_barber": "Mike",
        "last_visit": "2024-01-15",
        "preferences": ["short sides", "scissor cut"]
    },
    "mike_johnson": {
        "name": "Mike Johnson", 
        "phone": "555-0456",
        "email": "mike@email.com",
        "hair_type": "curly",
        "preferred_barber": "Sarah",
        "last_visit": "2024-01-20",
        "preferences": ["fade", "beard trim"]
    }
}

APPOINTMENTS_DB = [
    {
        "id": "apt001",
        "customer": "John Smith",
        "barber": "Mike",
        "date": "2024-02-15",
        "time": "10:00 AM",
        "service": "Haircut",
        "status": "confirmed"
    }
]

SERVICES_DB = {
    "haircut": {"name": "Haircut", "price": 35, "duration": 30},
    "beard_trim": {"name": "Beard Trim", "price": 20, "duration": 15},
    "shampoo": {"name": "Shampoo & Style", "price": 25, "duration": 20},
    "full_service": {"name": "Full Service Package", "price": 65, "duration": 60},
    "mustache_trim": {"name": "Mustache Trim", "price": 15, "duration": 10}
}

BARBER_SCHEDULE = {
    "Mike": {
        "monday": ["9:00 AM", "10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM"],
        "tuesday": ["9:00 AM", "10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM"],
        "friday": ["9:00 AM", "10:00 AM", "2:00 PM", "3:00 PM", "4:00 PM"]
    },
    "Sarah": {
        "monday": ["10:00 AM", "11:00 AM", "1:00 PM", "2:00 PM", "4:00 PM"],
        "wednesday": ["9:00 AM", "11:00 AM", "1:00 PM", "3:00 PM", "4:00 PM"],
        "friday": ["10:00 AM", "11:00 AM", "1:00 PM", "2:00 PM"]
    }
}

KNOWLEDGE_BASE = {
    "hair_care_tips": [
        "Wash hair 2-3 times per week to avoid over-drying",
        "Use conditioner to keep hair moisturized",
        "Regular trims every 4-6 weeks maintain healthy hair",
        "Use heat protectant before styling with hot tools"
    ],
    "styling_advice": [
        "Choose styles that complement your face shape",
        "Consider your lifestyle when selecting maintenance level",
        "Discuss your hair goals with your barber",
        "Bring reference photos for clear communication"
    ],
    "shop_policies": [
        "24-hour cancellation policy to avoid fees",
        "We accept cash, card, and mobile payments",
        "Walk-ins welcome but appointments recommended",
        "Children under 12 get 20% discount"
    ]
}


@tool
def get_customer_info(customer_identifier: str) -> str:
    """
    Retrieve customer information from the database using name, phone, or email.
    
    Args:
        customer_identifier: Customer name, phone number, or email address
    
    Returns:
        JSON string with customer information or error message
    """
    # Normalize identifier for search
    identifier = customer_identifier.lower().replace(" ", "_")
    
    # Search by key first
    if identifier in CUSTOMERS_DB:
        customer = CUSTOMERS_DB[identifier]
        return json.dumps({
            "status": "found",
            "customer": customer
        }, indent=2)
    
    # Search by phone or email
    for key, customer in CUSTOMERS_DB.items():
        if (customer.get("phone") == customer_identifier or 
            customer.get("email") == customer_identifier):
            return json.dumps({
                "status": "found", 
                "customer": customer
            }, indent=2)
    
    return json.dumps({
        "status": "not_found",
        "message": f"No customer found with identifier: {customer_identifier}"
    })

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the knowledge base for hair care tips, styling advice, and shop policies.
    
    Args:
        query: Search query for information
        
    Returns:
        Relevant information from knowledge base
    """
    query_lower = query.lower()
    results = []
    
    # Search hair care tips
    if any(word in query_lower for word in ["hair", "care", "wash", "condition"]):
        results.extend([
            "**Hair Care Tips:**"
        ] + KNOWLEDGE_BASE["hair_care_tips"])
    
    # Search styling advice
    if any(word in query_lower for word in ["style", "cut", "look", "face"]):
        results.extend([
            "**Styling Advice:**"
        ] + KNOWLEDGE_BASE["styling_advice"])
    
    # Search shop policies
    if any(word in query_lower for word in ["policy", "payment", "cancel", "price"]):
        results.extend([
            "**Shop Policies:**"
        ] + KNOWLEDGE_BASE["shop_policies"])
    
    if not results:
        results = [
            "Here's some general information:",
            "- We offer haircuts, beard trims, and styling services",
            "- Open Monday-Saturday 9AM-6PM",
            "- Book appointments online or call (555) 123-BARB"
        ]
    
    return "\n".join(results)

@tool
def get_appointment_status(customer_name: str, appointment_id: str = None) -> str:
    """
    Get current appointment status and details for a customer.
    
    Args:
        customer_name: Name of the customer
        appointment_id: Optional specific appointment ID
        
    Returns:
        Appointment details or status message
    """
    customer_appointments = [
        apt for apt in APPOINTMENTS_DB 
        if apt["customer"].lower() == customer_name.lower()
    ]
    
    if appointment_id:
        specific_apt = next(
            (apt for apt in APPOINTMENTS_DB if apt["id"] == appointment_id), 
            None
        )
        if specific_apt:
            return json.dumps({
                "status": "found",
                "appointment": specific_apt
            }, indent=2)
        else:
            return json.dumps({
                "status": "not_found",
                "message": f"Appointment {appointment_id} not found"
            })
    
    if customer_appointments:
        return json.dumps({
            "status": "found",
            "appointments": customer_appointments,
            "count": len(customer_appointments)
        }, indent=2)
    else:
        return json.dumps({
            "status": "no_appointments",
            "message": f"No appointments found for {customer_name}"
        })

@tool
def make_appointment(customer_name: str, service: str, preferred_date: str, 
                    preferred_time: str, barber_preference: str = None) -> str:
    """
    Create a new appointment for a customer.
    
    Args:
        customer_name: Name of the customer
        service: Type of service requested
        preferred_date: Preferred appointment date
        preferred_time: Preferred appointment time
        barber_preference: Optional preferred barber
        
    Returns:
        Appointment confirmation or alternative suggestions
    """
    # Normalize customer name
    customer_key = customer_name.lower().replace(" ", "_")
    
    # Check if customer exists
    if customer_key not in CUSTOMERS_DB:
        return f"Customer {customer_name} not found in our records. Please create a profile first."
    
    customer = CUSTOMERS_DB[customer_key]
    customer_phone = customer["phone"]
    
    # Check if preferred time is available
    available_times = check_availability(preferred_date, barber_preference)
    if preferred_time not in available_times:
        return f"The preferred time {preferred_time} is not available. Available times are: {', '.join(available_times)}"
    
    # Create appointment ID
    apt_id = f"apt{len(APPOINTMENTS_DB) + 1:03d}"
    
    # Add appointment to database
    new_appointment = {
        "id": apt_id,
        "customer": customer_name,
        "barber": barber_preference if barber_preference else "Available",
        "date": preferred_date,
        "time": preferred_time,
        "service": service,
        "status": "confirmed"
    }
    APPOINTMENTS_DB.append(new_appointment)
    
    # Send SMS notification
    sms_message = f"Dear {customer_name}, your appointment for {service} on {preferred_date} at {preferred_time} has been confirmed. Barber: {barber_preference if barber_preference else 'Available'}."
    sms_status = send_sms_notification(customer_phone, sms_message)
    
    return f"Appointment confirmed! {sms_status}"

@tool
def check_availability(date: str, barber_name: str = None) -> str:
    """
    Check available time slots for barbers on a specific date.
    
    Args:
        date: Date to check availability (format: YYYY-MM-DD or day name)
        barber_name: Optional specific barber to check
        
    Returns:
        Available time slots
    """
    # Convert date to day name for demo (simplified)
    day_mapping = {
        "monday": "monday", "tuesday": "tuesday", "wednesday": "wednesday",
        "thursday": "thursday", "friday": "friday", "saturday": "saturday"
    }
    
    day = date.lower()
    if day not in day_mapping:
        # Try to parse as date and get day name
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            day = date_obj.strftime("%A").lower()
        except:
            day = "monday"  # Default fallback
    
    availability = {}
    
    if barber_name:
        barber_name = barber_name.title()
        if barber_name in BARBER_SCHEDULE:
            slots = BARBER_SCHEDULE[barber_name].get(day, [])
            availability[barber_name] = slots
        else:
            return json.dumps({
                "status": "barber_not_found",
                "message": f"Barber {barber_name} not found",
                "available_barbers": list(BARBER_SCHEDULE.keys())
            })
    else:
        # Check all barbers
        for barber, schedule in BARBER_SCHEDULE.items():
            slots = schedule.get(day, [])
            if slots:
                availability[barber] = slots
    
    return json.dumps({
        "status": "available",
        "date": date,
        "day": day,
        "availability": availability
    }, indent=2)

@tool
def get_services_and_prices() -> str:
    """
    Get complete list of available services with prices and duration.
    
    Returns:
        List of all services with details
    """
    services_list = []
    
    for service_key, service_info in SERVICES_DB.items():
        services_list.append({
            "service": service_info["name"],
            "price": f"${service_info['price']}",
            "duration": f"{service_info['duration']} minutes"
        })
    
    return json.dumps({
        "status": "success",
        "services": services_list,
        "note": "Prices may vary based on hair length and complexity"
    }, indent=2)