import os
import asyncio
from crewai import Agent, Task, Crew, LLM

class GeoSupplyAgents:
    def __init__(self):
        print("🚀 Connecting to Google AI Studio (Gemini Engine)...")
        
        # Veilig ophalen van de API-key uit de omgevingsvariabelen (GitHub Secrets / Colab Secrets)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ ERROR: GEMINI_API_KEY is niet ingesteld in de omgevingsvariabelen!")

        # We gebruiken het geavanceerde Gemini 2.5 Flash model
        self.gemini_llm = LLM(
            model="gemini/gemini-2.5-flash",
            temperature=0.5,
            api_key=api_key
        )

    def geopolitical_analyst(self) -> Agent:
        """Agent 1: De Geopolitiek Analist (Risico's inschatten)"""
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
        """Agent 2: De Data Analist (Impact doorrekenen)"""
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
        """Agent 3: De HCSS Strategisch Adviseur (Beleidsadvies schrijven)"""
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

# --- DE TEST SIMULATIE (OM TE KIJKEN OF ZE HET DOEN) ---
async def run_test_simulation():
    # 1. Initialiseer de fabriek en maak de agents aan
    factory = GeoSupplyAgents()
    analyst = factory.geopolitical_analyst()
    cruncher = factory.data_cruncher()
    advisor = factory.policy_advisor()

    # 2. Definieer de keten van taken (De output van taak 1 stroomt door naar taak 2, etc.)
    taak_analyse = Task(
        description=(
            "Analyseer de geopolitieke spanningen tussen de EU en China. Wat gebeurt er "
            "als China besluit de export van Lithium naar de EU met 50% te beperken vanwege politieke motieven?"
        ),
        expected_output="Een geopolitieke risico-analyse van de situatie.",
        agent=analyst
    )

    taak_data = Task(
        description=(
            "Gebruik de geopolitieke analyse en schat in wat dit betekent voor de Europese "
            "batterij- en auto-industrie. Welke tekorten kunnen we op papier verwachten?"
        ),
        expected_output="Een kwantitatieve inschatting van de industriële impact.",
        agent=cruncher
    )

    taak_advies = Task(
        description=(
            "Neem de risico-analyse en de data-impact. Schrijf nu een HCSS Beleidsbrief (Policy Brief) "
            "voor de Nederlandse overheid met 3 concrete, strategische aanbevelingen om de afhankelijkheid te verkleinen."
        ),
        expected_output="Een professionele HCSS Policy Brief in het Nederlands met 3 strategische adviezen.",
        agent=advisor
    )

    # 3. Breng het hele team samen in een Crew
    crew = Crew(
        agents=[analyst, cruncher, advisor],
        tasks=[taak_analyse, taak_data, taak_advies],
        verbose=True
    )

    print("\n🎬 Start de volledige HCSS Multi-Agent simulatie via Gemini...")
    resultaat = await crew.kickoff_async()
    
    print("\n📜 ================= HET EINDRESULTAAT =================")
    print(resultaat)
    print("======================================================== 📜")

# Dit zorgt ervoor dat de code lokaal op je computer (buiten Colab) goed start
if __name__ == "__main__":
    asyncio.run(run_test_simulation())
