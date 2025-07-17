from crewai import Crew
from agents import BarberAgents
from tasks import BarberTasks

class BarberServiceCrew:
    def __init__(self, customer_name, service_request, customer_details=None, model="gpt-4o"):
        self.customer_name = customer_name
        self.service_request = service_request
        self.customer_details = customer_details
        self.model = model

    def run(self):
        agents = BarberAgents(model=self.model)
        tasks = BarberTasks()

        customer_service_manager = agents.customer_service_manager()
        appointment_specialist = agents.appointment_booking_specialist()
        service_consultant = agents.service_consultant()
        pricing_specialist = agents.pricing_payment_specialist()
        support_agent = agents.customer_support_agent()

        crew_tasks = []
        crew_agents = [customer_service_manager]

        if "appointment" in self.service_request.lower():
            crew_agents.append(appointment_specialist)
            crew_tasks.append(
                tasks.manage_appointment(
                    appointment_specialist,
                    self.customer_name,
                    self.customer_details.get("preferred_date", "flexible"),
                    self.customer_details.get("preferred_time", "flexible"),
                    self.customer_details.get("service_type", "haircut"),
                    self.customer_details.get("special_requests")
                )
            )

        if "recommend" in self.service_request.lower() or "service" in self.service_request.lower():
            crew_agents.append(service_consultant)
            crew_tasks.append(
                tasks.recommend_services(
                    service_consultant,
                    self.customer_details.get("profile", "new customer"),
                    self.customer_details.get("hair_type", "unknown"),
                    self.customer_details.get("lifestyle", "busy professional"),
                    self.customer_details.get("budget", "$50-100"),
                    self.customer_details.get("special_occasions")
                )
            )

        if "price" in self.service_request.lower() or "cost" in self.service_request.lower():
            crew_agents.append(pricing_specialist)
            crew_tasks.append(
                tasks.handle_pricing_inquiry(
                    pricing_specialist,
                    self.customer_details.get("services_interested", "haircut and beard trim"),
                    self.customer_details.get("package_deals", True),
                    self.customer_details.get("membership_status", "non-member"),
                    self.customer_details.get("pricing_questions")
                )
            )

        if "complaint" in self.service_request.lower() or "issue" in self.service_request.lower():
            crew_agents.append(support_agent)
            crew_tasks.append(
                tasks.resolve_customer_issue(
                    support_agent,
                    self.customer_details.get("issue_description", self.service_request),
                    self.customer_details.get("customer_history", "regular customer"),
                    self.customer_details.get("urgency", "medium"),
                    self.customer_details.get("preferred_resolution")
                )
            )

        if "information" in self.service_request.lower() or "hours" in self.service_request.lower():
            crew_tasks.append(
                tasks.provide_shop_information(
                    customer_service_manager,
                    self.customer_details.get("info_type", "general"),
                    self.customer_details.get("specific_questions")
                )
            )

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

        crew = Crew(
            agents=crew_agents,
            tasks=crew_tasks,
            verbose=True,
            memory=False
        )

        return crew.kickoff()


if __name__ == "__main__":
    print("\n==============================")
    print(" Welcome to BarberBot Crew")
    print("==============================")
    
    
    name = input("Enter your name: ")
    req = input("Enter what do you want to do: ")  #pricing or booking
    date = input("When do you want to visit: ")
    time = input("Enter your preferred time: ")
    type = input("Mention the service you want: ")
    spe_req = input("Any special requests: ")
    
    crew = BarberServiceCrew(
        customer_name= name,
        service_request= req,
        customer_details={
            "preferred_date": date,
            "preferred_time": time,
            "service_type": type,
            "special_requests": spe_req
        }
    )


    result = crew.run()

    print("\n==============================")
    print(" Response ✂️")
    print("==============================")
    print(result)
