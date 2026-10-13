### Step-by-Step Strategic Reasoning Procedure (Chain-of-Thought)

Follow this rigorous internal procedure before formulating the final JSON report:

#### Step 1: Metric Diagnostics & Bottleneck Identification
- Calculate and cross-reference key operational metrics:
  - **Acquisition Efficiency**: Monthly inbound leads vs website visitors (Visitor-to-Lead conversion rate: `inbound_leads / website_visitors * 100`).
  - **Sales Conversion**: Lead-to-customer conversion rate (`lead_to_customer_conversion_pct`).
  - **Retention Health**: Monthly churn rate (`monthly_churn_rate_pct`) and net revenue retention (`net_revenue_retention_pct`). Compare against healthy B2B benchmarks (<3-5% monthly churn, >100% NRR).
  - **CAC Payback**: Customer acquisition cost (`customer_acquisition_cost_usd`) vs average contract value (`average_contract_value_usd`).
- Identify the single most critical bottleneck constraining company growth. If churn is high, diagnose that acquisition cannot compound until retention is stabilized.

#### Step 2: Strategic Thesis & 30-Day Milestone
- Formulate a clear strategic thesis: a high-leverage hypothesis detailing how the company will stabilize the primary bottleneck while activating capital-efficient acquisition channels.
- Establish a realistic, measurable 30-day objective with specific percentage or volume targets.

#### Step 3: Growth Channel Ideation & Constraint Filtering
- Filter out any channel prohibited by `constraints.excluded_channels` (e.g., paid ad blitzes).
- Prioritize channels that leverage existing assets (`existing_channels`, ICP alignment, founder strengths) and respect team size and engineering constraints (e.g., no-code workflows, founder-led outreach, customer advocacy).

#### Step 4: Multi-Factor Channel Evaluation & Mathematical Scoring
Score candidate channels across 5 criteria (each scored on an integer scale from 0 to 100):
1. `score_impact` (35% weight / 0.35): Direct leverage on alleviating the primary bottleneck and driving revenue.
2. `score_fit` (25% weight / 0.25): ICP alignment, founder/team skillset compatibility, and synergy with existing channels.
3. `score_feasibility` (20% weight / 0.20): Ease of implementation given team size (e.g., 3 people) and limited engineering capacity.
4. `score_learning_speed` (10% weight / 0.10): How quickly leading indicators and feedback signals can be observed (days to signal).
5. `score_cost_efficiency` (10% weight / 0.10): Capital efficiency and expected ROI within the available budget.

*Scoring Precision Rule*: Use round numbers (multiples of 10, such as 60, 70, 80, 90) for sub-scores so arithmetic is clean and exact.
Calculate each channel's `priority_score` with strict mathematical accuracy:
`priority_score = round((0.35 * score_impact) + (0.25 * score_fit) + (0.20 * score_feasibility) + (0.10 * score_learning_speed) + (0.10 * score_cost_efficiency), 2)`

#### Step 5: Channel Specification & System Architecture
For each of the top 3 ranked channels:
- Define the channel as a **repeatable operational system** (e.g., automated trigger sequences, standardized outreach playbooks, weekly review cadences, or documented content flywheels).
- Provide concrete `supporting_evidence` directly referencing the company's quantitative input metrics.
- Define a high-fidelity `leading_kpi` and quantifiable target.
- Allocate `budget_usd` such that the sum of budgets across all 3 channels is strictly $\le$ `monthly_marketing_budget_usd`.
- Specify `time_to_signal_days` and 2-3 genuine operational risks.

#### Step 6: 30-Day Phased Execution Plan (4 Weeks)
Construct a progressive 4-week execution roadmap (`week` values 1, 2, 3, 4):
- **Week 1 (Days 1–7) - Audit & Instrumentation**: Baseline measurement, funnel bottleneck mapping, customer discovery/churn interviews, and tracking setup.
- **Week 2 (Days 8–14) - System Build & Collateral**: Build no-code automations, draft messaging sequences, create templates, and configure workflows.
- **Week 3 (Days 15–21) - Launch & Signal Detection**: Deploy initial workflows to small customer/prospect segments, conduct pilot tests, and collect leading indicator data.
- **Week 4 (Days 22–30) - Review, Iteration & SOP Institutionalization**: Analyze results against leading KPIs, optimize bottlenecks, and document standard operating procedures for ongoing execution.
- Every task must have a clear `owner` (e.g., "Founder", "Head of Growth", "Customer Success Lead"), a `due_day` (between 1 and 30), a quantifiable `success_metric`, and a tangible `deliverable`.

#### Step 7: Pre-Flight Verification Checklist
Before returning the JSON payload, verify:
- [x] Exactly 3 channels ranked 1, 2, and 3 with descending priority scores.
- [x] All 3 channel names are distinct.
- [x] No excluded channel is proposed.
- [x] Total channel budget $\le$ monthly marketing budget.
- [x] Priority scores match the mathematical weighted formula exactly.
- [x] Exactly 4 weeks (1, 2, 3, 4) in the 30-day action plan.
- [x] Every task `due_day` is an integer between 1 and 30.
- [x] Output is purely valid JSON without extra fields, text, or markdown code blocks.

