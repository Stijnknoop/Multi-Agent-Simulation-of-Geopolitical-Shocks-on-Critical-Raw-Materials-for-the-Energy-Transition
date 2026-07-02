import os
from crewai import Agent, LLM

class GeoSupplyAgents:
    def __init__(self):
        print("🚀 Connecting to Google AI Studio (Gemini Engine)...")
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ ERROR: GEMINI_API_KEY is niet ingesteld!")

        self.gemini_llm = LLM(
            model="gemini/gemini-2.5-flash",
            temperature=0.5,
            api_key=api_key
        )

    def geopolitical_analyst(self) -> Agent:
        """Agent 1: De Geopolitiek Analist"""
        return Agent(
            role="Senior Geopolitical Risk Analyst",
            goal="Analyze international conflicts, trade policies, and political shocks to predict supply chain disruptions.",
            backstory=(
                "You are an expert in geo-economics and international relations, specializing in "
                "resource weaponization. You understand how political tension between superpowers translates "
                "into export restrictions, tariffs, and maritime chokepoints."
            ),
            llm=self.gemini_llm,
            verbose=True,
            allow_delegation=False
        )

    def data_cruncher(self) -> Agent:
        """Agent 2: De Data Analist"""
        return Agent(
            role="Critical Materials Data Scientist",
            goal="Calculate the exact impact of supply disruptions on global production, reserves, and resources.",
            backstory=(
                "You are a data scientist specialized in mineral economics. You take geopolitical disruption "
                "scenarios and cross-reference them with market data to estimate supply shortages, production drops, "
                "and deficits for specific industrial regions."
            ),
            llm=self.gemini_llm,
            verbose=True,
            allow_delegation=False
        )

    def policy_advisor(self) -> Agent:
        """Agent 3: De HCSS Strategisch Adviseur"""
        return Agent(
            role="HCSS Strategic Policy Advisor",
            goal="Formulate actionable strategic advice and policy briefs for the EU and the Dutch government.",
            backstory=(
                "You are a top advisor at the Hague Centre for Strategic Studies. You translate complex "
                "geopolitical analysis and hard data metrics into high-level strategic policy briefs. "
                "Your recommendations focus on strategic autonomy, supply chain diversification, and national security."
            ),
            llm=self.gemini_llm,
            verbose=True,
            allow_delegation=False
        )
