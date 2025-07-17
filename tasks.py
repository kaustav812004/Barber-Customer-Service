from crewai import Task

class BarberTasks:

    def provide_shop_information(self, agent, info_type, questions):
        return Task(
            description=f"""Provide detailed shop information about '{info_type}' based on the customer's questions.
            Questions might include: {questions or 'none provided'}""",
            expected_output="A friendly and detailed explanation about the shop's services, hours, or general policies.",
            agent=agent,
            async_execution=False
        )

    def manage_appointment(self, agent, name, date, time, service_type, notes):
        return Task(
            description=f"""Book or update an appointment for {name} on {date} at {time} for service: {service_type}.
            Special notes: {notes or 'None'}""",
            expected_output="A confirmation of the appointment with time, date, service, and assigned barber (if available).",
            agent=agent,
            async_execution=False
        )

    def recommend_services(self, agent, profile, hair_type, lifestyle, budget, occasion):
        return Task(
            description=f"""Based on the customer profile '{profile}', hair type '{hair_type}', lifestyle '{lifestyle}',
            and budget '{budget}', recommend the most suitable grooming services. Special occasion: {occasion or 'None'}""",
            expected_output="A list of recommended grooming services with reasons.",
            agent=agent,
            async_execution=False
        )

    def handle_pricing_inquiry(self, agent, services, has_deals, membership_status, other_questions):
        return Task(
            description=f"""The customer is interested in the following services: {services}.
            They are a {membership_status}, looking for pricing details and deals (package available: {has_deals}).
            Other questions: {other_questions or 'None'}""",
            expected_output="Clear, transparent pricing information and explanations of any available packages.",
            agent=agent,
            async_execution=False
        )

    def resolve_customer_issue(self, agent, issue_description, history, urgency, resolution):
        return Task(
            description=f"""Handle a customer issue: {issue_description}.
            Customer history: {history}. Urgency: {urgency}. Preferred resolution: {resolution or 'not specified'}""",
            expected_output="A proposed resolution or apology that is fair and resolves the concern.",
            agent=agent,
            async_execution=False
        )
