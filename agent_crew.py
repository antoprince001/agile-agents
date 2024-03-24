from crewai import Agent, Task, Crew
import time

def create_product_owner_agent(llm):
    product_owner = Agent(
        role='Product Owner',
        goal='Define the project vision and prioritize features to maximize value for clients',
        backstory="""As the Product Owner, you are responsible for defining the project vision and ensuring alignment with client goals.
        Your decisions drive the direction of the project and determine which features are developed.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    return product_owner


def create_business_analyst_agent(llm):
    business_analyst = Agent(
        role='Business Analyst',
        goal='Analyze client requirements and translate them into clear, actionable user stories',
        backstory="""As the Business Analyst, your role is to understand and document client needs, transforming them into user stories that guide development.
        Your analyses ensure that the project team delivers solutions that meet client expectations.""",
        verbose=True,
        allow_delegation=True,
        llm=llm,
    )
    return business_analyst


def create_scrum_master_agent(llm):
    scrum_master = Agent(
        role='Scrum Master',
        goal='Facilitate sprint planning meetings and ensure alignment with project goals',
        backstory="""As the Scrum Master, your primary responsibility is to facilitate sprint planning meetings and ensure that the team understands the goals and priorities for the upcoming sprint.
        Your role is to guide the team through the planning process and foster collaboration.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )
    return scrum_master


def define_tasks(project_description, product_owner, business_analyst, scrum_master):
    # Tasks for Product Owner
    task1 = Task(
        description=f"""Define the project vision for {project_description}.Clearly articulate the project's purpose, goals, and target outcomes.""",
        expected_output="Text outlining the project vision and goal statements",
        agent=product_owner
    )

    # Tasks for Business Analyst
    task2 = Task(
        description=f"""{project_description} Gather requirements from stakeholders and translate them into clear, concise user stories.
        Ensure each user story captures a specific client need or feature request.""",
        expected_output="User stories with descriptions and acceptance criteria",
        agent=business_analyst
    )

    # Tasks for Scrum Master
    task3 = Task(
        description=f"""{project_description}. Facilitate the sprint planning meeting with the development team.
        Help the team select user stories from the backlog and create a detailed sprint plan.""",
        expected_output="Sprint plan outlining selected user stories and tasks for the upcoming sprint",
        agent=scrum_master
    )
    return task1, task2, task3


def create_crew(project_description, llm):
    # Instantiate agents
    product_owner = create_product_owner_agent(llm)
    business_analyst = create_business_analyst_agent(llm)
    scrum_master = create_scrum_master_agent(llm)

    # Instantiate your crew with a sequential process
    task1, task2, task3 = define_tasks(project_description, product_owner, business_analyst, scrum_master)
    crew = Crew(
        agents=[product_owner, business_analyst, scrum_master],
        tasks=[task1, task2],
        verbose=2  # You can set it to 1 or 2 to different logging levels
    )
    return crew


def generate_spring_plan(message, llm):
    crew = create_crew(message.content, llm)
    start_time = time.time()
    result = crew.kickoff()
    print(f"{time.time()-start_time}")
    print(result)
    return result
  