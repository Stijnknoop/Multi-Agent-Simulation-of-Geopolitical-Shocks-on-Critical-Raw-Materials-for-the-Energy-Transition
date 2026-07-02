import asyncio
import os
from datetime import datetime
from crewai import Task, Crew
from agents import GeoSupplyAgents

async def run_simulation():
    # 1. Initialize the agents
    factory = GeoSupplyAgents()
    analyst = factory.geopolitical_analyst()
    cruncher = factory.data_cruncher()
    advisor = factory.policy_advisor()

    # 2. Define the chain of tasks
    task_generate_scenario = Task(
        description=(
            "Generate a highly realistic, novel, and detailed geopolitical shock scenario involving "
            "critical raw materials (such as Lithium, Cobalt, Nickel, Graphite, or Rare Earth Elements) "
            "and their impact on the global energy transition. "
            "Do not reuse the exact examples provided below, but use them as a guide for tone, depth, and structural complexity:\n\n"
            "EXAMPLE 1 (Export Restrictions): China restricts Lithium exports to the EU by 50% due to escalating trade tensions.\n"
            "EXAMPLE 2 (Chokepoint Crisis): A military escalation in the Taiwan Strait blocks major maritime shipping lanes for 60 days.\n"
            "EXAMPLE 3 (Resource Nationalism): Chile, Argentina, and Bolivia form a lithium cartel and impose sudden 40% export quotas on Western markets.\n\n"
            "Create a completely new scenario (e.g., involving cyberattacks on mining infrastructure, nationalization of mines in Africa, "
            "environmental bans, or new bilateral monopoly alliances). Focus heavily on the strategic tension."
        ),
        expected_output="A detailed, 1-paragraph description of a novel geopolitical critical material crisis scenario.",
        agent=analyst
    )

    task_analysis = Task(
        description=(
            "Analyze the geopolitical risk of the scenario generated in the previous task. "
            "What are the immediate diplomatic tensions, state motivations, and systemic risks arising from this crisis?"
        ),
        expected_output="A comprehensive geopolitical risk analysis based on the generated scenario.",
        agent=analyst,
        context=[task_generate_scenario]
    )

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
        agents=[analyst, cruncher, advisor],
        tasks=[task_generate_scenario, task_analysis, task_data, task_advice],
        verbose=True
    )

    print("\n🎬 Starting the full HCSS Multi-Agent Autonomous Simulation via Gemini...")
    result = await crew.kickoff_async()
    
    # 4. NEW: Save all outputs into a structured Markdown file inside the 'results' folder
    print("\n💾 Saving simulation outputs to the results folder...")
    os.makedirs("results", exist_ok=True)
    
    # Create a unique filename based on the current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/simulation_report_{timestamp}.md"
    
    # Build a comprehensive Markdown report pulling data from each specific task output
    markdown_report = f"""# HCSS Geopolitical Shock Simulation Report
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 1. Dynamic Crisis Scenario
{task_generate_scenario.output.raw if task_generate_scenario.output else "No scenario generated."}

## 2. Geopolitical Risk Analysis
{task_analysis.output.raw if task_analysis.output else "No analysis generated."}

## 3. Industrial & Supply Chain Impact Assessment
{task_data.output.raw if task_data.output else "No data impact assessment generated."}

## 4. HCSS Policy Brief & Strategic Recommendations
{task_advice.output.raw if task_advice.output else "No policy brief generated."}
"""
    
    # Write the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_report)
        
    print(f"✅ Success! Full report successfully saved to: {filename}")

    print("\n📜 ================= FINAL SIMULATION REPORT =================")
    print(result)
    print("============================================================== 📜")

if __name__ == "__main__":
    asyncio.run(run_simulation())
