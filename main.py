import os
from crewai import Crew
from textwrap import dedent
from agents import BarberAgents
from tasks import BarberTasks

from dotenv import load_dotenv
load_dotenv()

# Ensure OpenAI API key is set
if not os.getenv("AZURE_OPENAI_API_KEY"):
    raise ValueError("Please set your OPENAI_API_KEY in the .env file")

class BarberServiceCrew:
    def __init__(self, customer_name, service_request, customer_details=None, model="gpt-4o"):
        self.customer_name = customer_name
        self.service_request = service_request
        self.customer_details = customer_details or {}
        self.model = model

    def run(self):
        try:
            # Define your custom agents and tasks
            agents = BarberAgents(model=self.model)
            tasks = BarberTasks()

            # Initialize all agents
            customer_service_manager = agents.customer_service_manager()
            appointment_specialist = agents.appointment_booking_specialist()
            service_consultant = agents.service_consultant()
            pricing_specialist = agents.pricing_payment_specialist()
            support_agent = agents.customer_support_agent()

            # Determine which tasks to execute based on service request type
            crew_tasks = []
            crew_agents = [customer_service_manager]

            if "appointment" in self.service_request.lower():
                crew_agents.append(appointment_specialist)
                crew_tasks.append(
                    tasks.manage_appointment(
                        appointment_specialist,
                        self.customer_name,
                        self.customer_details.get('preferred_date', 'flexible'),
                        self.customer_details.get('preferred_time', 'flexible'),
                        self.customer_details.get('service_type', 'haircut'),
                        self.customer_details.get('special_requests')
                    )
                )

            if "recommend" in self.service_request.lower() or "service" in self.service_request.lower():
                crew_agents.append(service_consultant)
                crew_tasks.append(
                    tasks.recommend_services(
                        service_consultant,
                        self.customer_details.get('profile', 'new customer'),
                        self.customer_details.get('hair_type', 'unknown'),
                        self.customer_details.get('lifestyle', 'busy professional'),
                        self.customer_details.get('budget', '$50-100'),
                        self.customer_details.get('special_occasions')
                    )
                )

            if "price" in self.service_request.lower() or "cost" in self.service_request.lower():
                crew_agents.append(pricing_specialist)
                crew_tasks.append(
                    tasks.handle_pricing_inquiry(
                        pricing_specialist,
                        self.customer_details.get('services_interested', 'haircut and beard trim'),
                        self.customer_details.get('package_deals', True),
                        self.customer_details.get('membership_status', 'non-member'),
                        self.customer_details.get('pricing_questions')
                    )
                )

            if "complaint" in self.service_request.lower() or "issue" in self.service_request.lower():
                crew_agents.append(support_agent)
                crew_tasks.append(
                    tasks.resolve_customer_issue(
                        support_agent,
                        self.customer_details.get('issue_description', self.service_request),
                        self.customer_details.get('customer_history', 'regular customer'),
                        self.customer_details.get('urgency', 'medium'),
                        self.customer_details.get('preferred_resolution')
                    )
                )

            if "information" in self.service_request.lower() or "hours" in self.service_request.lower():
                crew_tasks.append(
                    tasks.provide_shop_information(
                        customer_service_manager,
                        self.customer_details.get('info_type', 'general'),
                        self.customer_details.get('specific_questions')
                    )
                )

            # If no specific tasks identified, provide general service consultation
            if not crew_tasks:
                crew_agents.append(service_consultant)
                crew_tasks.append(
                    tasks.recommend_services(
                        service_consultant,
                        "general inquiry",
                        "unknown",
                        "unknown",
                        "flexible",
                        None
                    )
                )

            # Create and run the crew
            crew = Crew(
                agents=crew_agents,
                tasks=crew_tasks,
                verbose=True,
                memory=False,  # Disable memory to avoid Pydantic issues
                embedder={
                    "provider": "openai",
                    "config": {
                        "model": "text-embedding-3-small"
                    }
                }
            )

            result = crew.kickoff()
            return result

        except Exception as e:
            print(f"Error running crew: {str(e)}")
            return f"Sorry, we encountered an error processing your request: {str(e)}"


# Interactive customer service interface
def interactive_mode():
    print("## Welcome to Premier Barber Shop Customer Service")
    print('=' * 50)
    
    customer_name = input("What's your name? ")
    
    print(f"\nHi {customer_name}! How can we help you today?")
    print("We can help with:")
    print("• Booking appointments")
    print("• Service recommendations") 
    print("• Pricing information")
    print("• Resolving issues")
    print("• General shop information")
    
    service_request = input("\nPlease describe what you need: ")
    
    # Collect additional details based on request type
    customer_details = {}
    
    if "appointment" in service_request.lower():
        customer_details['preferred_date'] = input("Preferred date (or 'flexible'): ")
        customer_details['preferred_time'] = input("Preferred time (or 'flexible'): ")
        customer_details['service_type'] = input("What service do you need? ")
        special_req = input("Any special requests? (optional): ")
        if special_req:
            customer_details['special_requests'] = special_req
    
    elif "recommend" in service_request.lower() or "service" in service_request.lower():
        customer_details['hair_type'] = input("What's your hair type? (curly/straight/wavy/thick/thin): ")
        customer_details['lifestyle'] = input("Describe your lifestyle: ")
        customer_details['budget'] = input("What's your budget range? ")
        occasion = input("Any special occasions coming up? (optional): ")
        if occasion:
            customer_details['special_occasions'] = occasion
    
    elif "price" in service_request.lower():
        customer_details['services_interested'] = input("Which services are you interested in? ")
        customer_details['membership_status'] = input("Are you a member? (yes/no): ")
    
    return BarberServiceCrew(customer_name, service_request, customer_details)


# Example usage functions
def example_appointment_booking():
    """Example: Customer wants to book an appointment"""
    customer_details = {
        'preferred_date': 'next Friday',
        'preferred_time': '2 PM',
        'service_type': 'haircut and beard trim',
        'special_requests': 'need to be done quickly, have meeting after'
    }
    
    crew = BarberServiceCrew(
        customer_name="John Smith",
        service_request="I need to book an appointment",
        customer_details=customer_details
    )
    return crew.run()


def example_service_recommendation():
    """Example: Customer wants service recommendations"""
    customer_details = {
        'hair_type': 'thick and curly',
        'lifestyle': 'busy executive, travel frequently',
        'budget': '$80-120',
        'special_occasions': 'wedding next month'
    }
    
    crew = BarberServiceCrew(
        customer_name="Mike Johnson",
        service_request="I need recommendations for services",
        customer_details=customer_details
    )
    return crew.run()


def example_pricing_inquiry():
    """Example: Customer wants pricing information"""
    customer_details = {
        'services_interested': 'full grooming package',
        'membership_status': 'non-member',
        'package_deals': True,
        'pricing_questions': 'Do you offer monthly packages?'
    }
    
    crew = BarberServiceCrew(
        customer_name="David Wilson",
        service_request="What are your prices?",
        customer_details=customer_details
    )
    return crew.run()


# Main execution
if __name__ == "__main__":
    import sys
    
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "interactive":
            # Interactive mode
            crew = interactive_mode()
            result = crew.run()
            
            print("\n" + "=" * 50)
            print("## Customer Service Response")
            print("=" * 50)
            print(result)
            
        elif len(sys.argv) > 1 and sys.argv[1] == "example":
            # Run example scenarios
            print("Running example scenarios...\n")
            
            print("1. Appointment Booking Example:")
            print("-" * 30)
            result1 = example_appointment_booking()
            print(result1)
            
            print("\n2. Service Recommendation Example:")
            print("-" * 35)
            result2 = example_service_recommendation()
            print(result2)
            
            print("\n3. Pricing Inquiry Example:")
            print("-" * 28)
            result3 = example_pricing_inquiry()
            print(result3)
            
        else:
            # Default interactive mode
            crew = interactive_mode()
            result = crew.run()
            
            print("\n" + "=" * 50)
            print("## Customer Service Response")
            print("=" * 50)
            print(result)
            
    except KeyboardInterrupt:
        print("\nGoodbye! Thank you for visiting Premier Barber Shop!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please try again or contact support.")