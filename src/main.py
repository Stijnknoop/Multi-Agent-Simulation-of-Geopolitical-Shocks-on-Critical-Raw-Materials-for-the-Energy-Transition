import asyncio
import os
from datetime import datetime
from crewai import Task, Crew
from agents import GeoSupplyAgents

def load_scraped_data() -> str:
    """Reads the scraped Wikipedia data to provide real-world context to the agents."""
    csv_path = "data/lithium_comprehensive.csv"
    if os.path.exists(csv_path):
        print(f"📈 Successfully loaded scraped data from {csv_path}")
        with open(csv_path, "r", encoding="utf-8") as f:
            # Loading the first 2000 characters to keep the prompt clean and efficient
            return f.read(2000)
    else:
        print("⚠️ Warning: No scraped data found at data/lithium_comprehensive.csv. Using fallback generic context.")
        return "Standard critical raw material baseline data (Lithium, production concentrated in Australia, Chile, China)."

async def run_simulation():
    # Load the actual data scraped in Week 1
    raw_material_data = load_scraped_data()

    # 1. Initialize all 4 agents
    factory = GeoSupplyAgents()
    futurist = factory.scenario_generator()
    analyst = factory.geopolitical_analyst()
    cruncher = factory.data_cruncher()
    advisor = factory.policy_advisor()

    # 2. Define the chain of tasks
    
    # TASK 1: The Futurist generates the scenario using your comprehensive prompt template
    task_generate_scenario = Task(
        description=(
            f"Review the following real-world Lithium market data scraped from Wikipedia:\n"
            f"```csv\n{raw_material_data}\n```\n\n"
            "Generate a highly realistic, novel, and detailed geopolitical shock scenario involving "
            "critical raw materials (such as Lithium, Cobalt, Nickel, Graphite, or Rare Earth Elements) "
            "and their impact on the global energy transition. If using Lithium, ground it in the scraped CSV data.\n\n"
            "CRITICAL CONSTRAINT: The scenario description MUST be concise and CANNOT exceed 150 words total.\n\n"
            "Do not reuse the exact examples provided below, but use them as a guide for tone, depth, and structural complexity:\n"
            "EXAMPLE 1 (Export Restrictions): China restricts Lithium exports to the EU by 50% due to escalating trade tensions.\n"
            "EXAMPLE 2 (Chokepoint Crisis): A military escalation in the Taiwan Strait blocks major maritime shipping lanes for 60 days.\n"
            "EXAMPLE 3 (Resource Nationalism): Chile, Argentina, and Bolivia form a lithium cartel and impose sudden 40% export quotas on Western markets.\n\n"
            "Create a completely new scenario (e.g., involving cyberattacks on mining infrastructure, nationalization of mines in Africa, "
            "environmental bans, or new bilateral monopoly alliances). Focus heavily on the strategic tension."
        ),
        expected_output="A detailed, single-paragraph description of a novel geopolitical critical material crisis scenario under 150 words.",
        agent=futurist # Assigned to the Strategic Futurist
    )

    # TASK 2: Analyze the generated scenario
    task_analysis = Task(
        description=(
            "Analyze the geopolitical risk of the scenario generated in the previous task. "
            "What are the immediate diplomatic tensions, state motivations, and systemic risks arising from this crisis?"
        ),
        expected_output="A comprehensive geopolitical risk analysis based on the generated scenario.",
        agent=analyst,
        context=[task_generate_scenario]
    )

    # TASK 3: Estimate industrial impact
    task_data = Task(
        description=(
            "Based on the generated crisis scenario and the subsequent geopolitical analysis, estimate the quantitative "
            "consequences for the European green technology and automotive industries. What supply deficits, production drops, "
            "or market vulnerabilities can be expected?"
        ),
        expected_output="A quantitative assessment of the industrial and supply chain impact.",
        agent=cruncher,
        context=[task_generate_scenario, task_analysis]
    )

    # TASK 4: Formulate HCSS Policy Brief
    task_advice = Task(
        description=(
            "Review the entire simulation history (the generated crisis, the risk analysis, and the data impact). "
            "Write an official HCSS Policy Brief tailored for the Dutch government and the EU Commission, providing "
            "3 concrete, actionable strategic recommendations to mitigate these specific risks and increase strategic autonomy."
        ),
        expected_output="A professional, executive-ready HCSS Policy Brief containing 3 actionable strategic recommendations.",
        agent=advisor,
        context=[task_data]
    )

    # 3. Assemble the team into a Crew
    crew = Crew(
        agents=[futurist, analyst, cruncher, advisor],
        tasks=[task_generate_scenario, task_analysis, task_data, task_advice],
        verbose=True
    )

    print("\n🎬 Starting the full HCSS Multi-Agent Autonomous Simulation via Gemini...")
    result = await crew.kickoff_async()
    
    # 4. Save all outputs into a structured Markdown file inside the 'results' folder
    print("\n💾 Saving simulation outputs to the results folder...")
    os.makedirs("results", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/simulation_report_{timestamp}.md"
    
    markdown_report = f"""# HCSS Geopolitical Shock Simulation Report
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 1. Dynamic Crisis Scenario (Generated by Strategic Futurist)
{task_generate_scenario.output.raw if task_generate_scenario.output else "No scenario generated."}

## 2. Geopolitical Risk Analysis (Analyzed by Senior Analyst)
{task_analysis.output.raw if task_analysis.output else "No analysis generated."}

## 3. Industrial & Supply Chain Impact Assessment (Calculated by Data Scientist)
{task_data.output.raw if task_data.output else "No data impact assessment generated."}

## 4. HCSS Policy Brief & Strategic Recommendations (Authored by Policy Advisor)
{task_advice.output.raw if task_advice.output else "No policy brief generated."}
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_report)
        
    print(f"✅ Success! Full report successfully saved to: {filename}")

if __name__ == "__main__":
    asyncio.run(run_simulation())
