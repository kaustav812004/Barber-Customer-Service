from crewai import Agent
from langchain_openai import AzureChatOpenAI
from tools.barber_tools import (
    get_customer_info,
    search_knowledge_base, 
    get_appointment_status,
    make_appointment,
    check_availability,
    get_services_and_prices
)

import os
from dotenv import load_dotenv
load_dotenv()

class BarberAgents:
    def __init__(self, model="gpt-4o"):
        """Initialize with Azure OpenAI LLM or fallback to OpenAI"""
        try:
            # Try Azure OpenAI first
            if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
                print("Initializing Azure OpenAI...")
                self.llm = AzureChatOpenAI(
                    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", model),
                    temperature=0.7,
                    max_tokens=1000,
                    timeout=60,
                    max_retries=3
                )
           
            
            # Test the LLM connection
            test_response = self.llm.invoke("Hello")
            print(f"LLM connection successful: {test_response.content[:50]}...")
            
        except Exception as e:
            print(f"Error initializing LLM: {str(e)}")
            print("Please check your configuration:")
            print(f"- AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
            print(f"- AZURE_OPENAI_API_KEY: {'Set' if os.getenv('AZURE_OPENAI_API_KEY') else 'Not set'}")
            print(f"- OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
            raise

    def customer_service_manager(self):
        """Customer Service Manager Agent - Handles customer inquiries and service requests"""
        return Agent(
            role="Customer Service Manager",
            goal="Provide excellent customer service by helping customers with appointments, answering questions about services, and resolving any issues they may have",
            backstory="""You are an experienced customer service manager at a premium barber shop. 
            You have years of experience in the beauty and grooming industry and pride yourself on 
            providing personalized, friendly service. You know all about hair care, styling trends, 
            and salon operations. You're skilled at handling appointments, managing customer 
            expectations, and ensuring every customer leaves satisfied.""",
            tools=[
                get_customer_info,
                search_knowledge_base,
                get_appointment_status,
                make_appointment,
                check_availability,
                get_services_and_prices
            ],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3,  # Limit iterations
            max_execution_time=120  # 2 minutes timeout
        )

    def appointment_booking_specialist(self):
        """Appointment Scheduler Agent - Specializes in booking and managing appointments"""
        return Agent(
            role="Appointment Booking Specialist",
            goal="Efficiently schedule appointments, manage the booking calendar, and ensure optimal time slot utilization for all barbers",
            backstory="""You are a detail-oriented appointment scheduler with excellent organizational skills. 
            You understand the importance of time management in a busy barber shop and work to minimize 
            wait times while maximizing barber productivity. You're familiar with each barber's 
            specialties and can recommend the best match for each customer's needs.""",
            tools=[
                check_availability,
                make_appointment,
                get_appointment_status,
                get_customer_info
            ],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=120
        )

    def service_consultant(self):
        """Hair Care Consultant Agent - Provides expert advice on hair care and styling"""
        return Agent(
            role="Service Consultant", 
            goal="Provide expert hair care advice, recommend appropriate services, and educate customers about proper hair maintenance",
            backstory="""You are a certified hair care specialist with extensive knowledge of different 
            hair types, styling techniques, and hair care products. You stay updated with the latest 
            trends and techniques in the industry. You're passionate about helping customers achieve 
            their desired look while maintaining healthy hair.""",
            tools=[
                search_knowledge_base,
                get_services_and_prices,
                get_customer_info
            ],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=120
        )

    def pricing_payment_specialist(self):
        """Pricing and Payment Specialist - Handles pricing inquiries and payment processing"""
        return Agent(
            role="Pricing and Payment Specialist",
            goal="Provide accurate pricing information, explain payment options, and handle billing inquiries with transparency and professionalism",
            backstory="""You are a knowledgeable pricing specialist who ensures customers understand 
            all costs upfront. You're experienced in explaining service packages, membership benefits, 
            and promotional offers. You handle all payment-related questions with clarity and help 
            customers find the best value for their needs.""",
            tools=[
                get_services_and_prices,
                search_knowledge_base,
                get_customer_info
            ],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=120
        )

    def customer_support_agent(self):
        """Customer Support Agent - Resolves issues and handles complaints"""
        return Agent(
            role="Customer Support Agent",
            goal="Resolve customer issues promptly and professionally, ensure customer satisfaction, and maintain positive relationships",
            backstory="""You are an empathetic customer support specialist with excellent problem-solving skills. 
            You have experience handling various customer concerns and complaints in the service industry. 
            You're skilled at de-escalating tense situations and finding mutually beneficial solutions that 
            maintain customer loyalty while protecting business interests.""",
            tools=[
                get_customer_info,
                get_appointment_status,
                search_knowledge_base,
                make_appointment
            ],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=120
        )


# main.py - Updated version with better error handling
import os
from crewai import Crew
from textwrap import dedent
from agents import BarberAgents
from tasks import BarberTasks

from dotenv import load_dotenv
load_dotenv()

# Validate environment variables
required_env_vars = [
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_DEPLOYMENT_NAME"
]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

class BarberServiceCrew:
    def __init__(self, customer_name, service_request, customer_details=None, model="gpt-4o"):
        self.customer_name = customer_name
        self.service_request = service_request
        self.customer_details = customer_details or {}
        self.model = model

    def run(self):
        try:
            print(f"Initializing barber service crew for {self.customer_name}...")
            
            # Define your custom agents and tasks
            agents = BarberAgents(model=self.model)
            tasks = BarberTasks()

            # Initialize all agents
            customer_service_manager = agents.customer_service_manager()
            
            # Start with a simple single-agent setup for testing
            crew_tasks = []
            crew_agents = [customer_service_manager]

            # Add a simple general information task
            crew_tasks.append(
                tasks.provide_shop_information(
                    customer_service_manager,
                    "general",
                    self.service_request
                )
            )

            print("Creating crew...")
            # Create and run the crew with minimal configuration
            crew = Crew(
                agents=crew_agents,
                tasks=crew_tasks,
                verbose=True,
                memory=False,  # Disable memory to avoid issues
                # Remove embedder configuration for now
            )

            print("Starting crew execution...")
            result = crew.kickoff()
            return result

        except Exception as e:
            error_msg = f"Error running crew: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            return error_msg


# Test function to check environment setup
def test_environment():
    """Test the environment setup before running the main application"""
    print("Testing environment setup...")
    
    # Check environment variables
    env_vars = {
        "AZURE_OPENAI_API_KEY": os.getenv("AZURE_OPENAI_API_KEY"),
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "AZURE_OPENAI_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        "AZURE_OPENAI_API_VERSION": os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    }
    
    for key, value in env_vars.items():
        if value:
            if "API_KEY" in key:
                print(f"✓ {key}: ***{value[-4:]}")  # Show last 4 characters
            else:
                print(f"✓ {key}: {value}")
        else:
            print(f"✗ {key}: Not set")
    
    # Test LLM connection
    try:
        print("\nTesting LLM connection...")
        agents = BarberAgents()
        print(" LLM connection successful")
        return True
    except Exception as e:
        print(f" LLM connection failed: {str(e)}")
        return False


# Simple test run
def simple_test():
    """Run a simple test with minimal complexity"""
    if not test_environment():
        return "Environment test failed"
    
    crew = BarberServiceCrew(
        customer_name="Test Customer",
        service_request="What are your shop hours?",
        customer_details={}
    )
    return crew.run()


# Main execution
if __name__ == "__main__":
    import sys
    
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "test":
            # Run simple test
            print("Running simple test...")
            result = simple_test()
            print("\n" + "=" * 50)
            print("## Test Result")
            print("=" * 50)
            print(result)
            
        elif len(sys.argv) > 1 and sys.argv[1] == "env":
            # Test environment only
            test_environment()
            
        else:
            # Run environment test first
            if not test_environment():
                print("Please fix environment issues before running the application.")
                sys.exit(1)
            
            # Run the application
            print("\n" + "=" * 50)
            print("## Starting Barber Customer Service")
            print("=" * 50)
            
            crew = BarberServiceCrew(
                customer_name="John Smith",
                service_request="I need information about your services",
                customer_details={}
            )
            result = crew.run()
            
            print("\n" + "=" * 50)
            print("## Customer Service Response")
            print("=" * 50)
            print(result)
            
    except KeyboardInterrupt:
        print("\nGoodbye! Thank you for visiting Premier Barber Shop!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        print("Please try again or contact support.")