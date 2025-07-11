from crewai import Task
from textwrap import dedent

class BarberTasks:
    def manage_appointment(self, agent, customer_name, preferred_date, preferred_time, service_type, special_requests=None):
        """Task for managing customer appointments"""
        return Task(
            description=dedent(f"""
                Help {customer_name} manage their appointment request.
                
                Customer Details:
                - Preferred Date: {preferred_date}
                - Preferred Time: {preferred_time}
                - Service Type: {service_type}
                - Special Requests: {special_requests or 'None'}
                
                Tasks to complete:
                1. Check customer information in the database
                2. Verify service availability and pricing
                3. Check barber availability for the requested date/time
                4. If requested slot is available, book the appointment
                5. If not available, suggest alternative times
                6. Provide confirmation details including:
                   - Appointment ID
                   - Date and time
                   - Service details and duration
                   - Barber assigned
                   - Total cost
                   - Any preparation instructions
            """),
            agent=agent,
            expected_output="A complete appointment confirmation or alternative suggestions with all relevant details"
        )

    def recommend_services(self, agent, customer_profile, hair_type, lifestyle, budget, special_occasions=None):
        """Task for providing service recommendations"""
        return Task(
            description=dedent(f"""
                Provide personalized service recommendations for a customer.
                
                Customer Profile:
                - Profile: {customer_profile}
                - Hair Type: {hair_type}
                - Lifestyle: {lifestyle}
                - Budget: {budget}
                - Special Occasions: {special_occasions or 'None'}
                
                Tasks to complete:
                1. Get current service offerings and prices
                2. Search knowledge base for relevant hair care advice
                3. Consider customer's hair type and lifestyle
                4. Recommend appropriate services within budget
                5. Provide styling advice and maintenance tips
                6. Include information about:
                   - Recommended services and why
                   - Estimated costs
                   - Maintenance requirements
                   - Timeline for special occasions if applicable
                   - Hair care tips specific to their hair type
            """),
            agent=agent,
            expected_output="Comprehensive service recommendations with pricing, maintenance advice, and personalized tips"
        )

    def handle_pricing_inquiry(self, agent, services_interested, package_deals, membership_status, pricing_questions=None):
        """Task for handling pricing and payment inquiries"""
        return Task(
            description=dedent(f"""
                Handle customer pricing inquiry and provide transparent cost information.
                
                Inquiry Details:
                - Services Interested: {services_interested}
                - Package Deals Interest: {package_deals}
                - Membership Status: {membership_status}
                - Specific Questions: {pricing_questions or 'General pricing'}
                
                Tasks to complete:
                1. Get complete service pricing information
                2. Calculate costs for requested services
                3. Explain any package deals or discounts available
                4. Provide membership benefits if applicable
                5. Search knowledge base for payment policies
                6. Include information about:
                   - Individual service prices
                   - Package deals and savings
                   - Payment methods accepted
                   - Cancellation policies
                   - Membership benefits
                   - Any current promotions
            """),
            agent=agent,
            expected_output="Complete pricing breakdown with payment options, policies, and potential savings"
        )

    def resolve_customer_issue(self, agent, issue_description, customer_history, urgency, preferred_resolution=None):
        """Task for resolving customer complaints and issues"""
        return Task(
            description=dedent(f"""
                Resolve customer issue with empathy and professionalism.
                
                Issue Details:
                - Issue Description: {issue_description}
                - Customer History: {customer_history}
                - Urgency Level: {urgency}
                - Preferred Resolution: {preferred_resolution or 'Not specified'}
                
                Tasks to complete:
                1. Get customer information and history
                2. Understand the specific issue thoroughly
                3. Check any relevant appointments or services
                4. Research shop policies that apply
                5. Propose appropriate solutions
                6. Provide resolution that includes:
                   - Acknowledgment of the issue
                   - Explanation of what happened (if known)
                   - Specific resolution steps
                   - Compensation if appropriate
                   - Steps to prevent future issues
                   - Follow-up plan if needed
            """),
            agent=agent,
            expected_output="Professional resolution with clear action steps and appropriate compensation if needed"
        )

    def provide_shop_information(self, agent, info_type, specific_questions=None):
        """Task for providing general shop information"""
        return Task(
            description=dedent(f"""
                Provide comprehensive shop information to the customer.
                
                Information Request:
                - Type of Information: {info_type}
                - Specific Questions: {specific_questions or 'General information'}
                
                Tasks to complete:
                1. Search knowledge base for relevant shop information
                2. Get current service offerings and prices
                3. Check barber availability and schedules
                4. Provide comprehensive information including:
                   - Shop hours and location
                   - Services offered
                   - Staff information
                   - Policies (cancellation, payment, etc.)
                   - Contact information
                   - Any special programs or memberships
                   - Current promotions
                   - Booking procedures
            """),
            agent=agent,
            expected_output="Complete shop information addressing all customer questions with helpful details"
        )