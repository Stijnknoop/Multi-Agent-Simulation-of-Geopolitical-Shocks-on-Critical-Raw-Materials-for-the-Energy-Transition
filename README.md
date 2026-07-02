# Autonomous Multi-Agent Simulation of Geopolitical Shocks on Critical Raw Materials

An end-to-end DataOps and GenAI simulation platform built as a strategic portfolio project for the **Hague Centre for Strategic Studies (HCSS)**. This platform automates the pipeline from critical raw material data collection to autonomous geopolitical shock generation, industrial impact analysis, and strategic policy formulation.

The entire system is powered by **CrewAI** and **Google Gemini 2.5 Flash**, fully containerized using **Docker**, and orchestrated via **GitHub Actions**.

---

## 🚀 Project Overview

The global energy transition relies heavily on secure supply chains for critical raw materials. This project simulates unexpected geopolitical and economic "shocks" to stress-test Western supply chains (specifically focusing on **Lithium and batteries**) and autonomously generates executive-ready strategic advice.

### Key Capabilities:
* **Automated Data Scraping (Week 1):** A Python-based pipeline that dynamically scrapes live market, production, and reserve data from global sources (e.g., Wikipedia) and saves it as structured data.
* **Autonomous Think Tank (Week 2):** A coordinated crew of 4 specialized AI agents that ingest real-world data, simulate strategic crises, calculate industrial deficits, and formulate policy briefs.
* **Production-Ready Containerization (Week 3):** Fully containerized using Docker with pinned dependencies (`requirements.txt`), ensuring 100% reproducible environments for cloud deployment.

---

## 🧠 Multi-Agent Architecture (The Crew)

The simulation uses a sequential multi-agent architecture where the output of each agent serves as the context for the next:

1. **Strategic Foresight Expert (Futurist):** Ingests the scraped Lithium data and designs a highly realistic, novel, and concise geopolitical shock scenario (restricted to <150 words) targeting supply vulnerabilities.
2. **Senior Geopolitical Risk Analyst:** Evaluates the political motivations, systemic diplomatic risks, and international tensions arising from the simulated crisis.
3. **Critical Materials Data Scientist:** Cross-references the crisis scenario with baseline production metrics to quantitatively assess supply deficits and industrial dropouts in European tech/automotive sectors.
4. **HCSS Strategic Policy Advisor:** Synthesizes the quantitative and qualitative findings into an official HCSS Policy Brief containing 3 highly actionable strategic recommendations for the Dutch government and the EU Commission.

---

## 📊 Where to Find the Results?

Every time the simulation runs, a comprehensive, timestamped Markdown report is automatically generated and saved directly to the repository.

You can find all generated intelligence reports in the **[`results/`](./results)** directory.

Each report is structured as follows:
* **`results/simulation_report_YYYYMMDD_HHMMSS.md`**
  1. Dynamic Crisis Scenario (Strategic Headline)
  2. Geopolitical Risk Analysis
  3. Industrial & Supply Chain Impact Assessment
  4. HCSS Policy Brief & 3 Actionable Strategic Recommendations

---

## 🛠️ How to Run the Infrastructure

### Option 1: Via GitHub Actions (No local setup required)
This repository uses automated GitHub Workflows to run the architecture in a clean cloud environment:
1. Navigate to the **Actions** tab in this repository.
2. Select **Run Live Data Scraper** to update the raw material data.
3. Select **Run AI Agent Simulation** and click *Run workflow* to trigger the autonomous AI think tank. The newly generated report will be committed directly back into the `results/` folder.

### Option 2: Locally via Docker (Fully Containerized)
To run the simulation locally without worrying about Python dependencies, build and run the Docker container:

```bash
# 1. Build the Docker Image
docker build -t hcss-ai-simulation .

# 2. Run the Container (Injecting your Gemini API Key safely)
docker run -e GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE" -v $(pwd)/results:/app/results hcss-ai-simulation
