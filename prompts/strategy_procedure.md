Internal Problem-Solving Procedure:
1. Assess the supplied business metrics (acquisition, conversion, retention, monetization).
2. Identify the most important bottlenecks and cite the exact input metrics supporting each finding.
3. Generate plausible growth-channel candidates.
4. Score candidates across the 5 evaluation criteria (each scored 0 to 100):
   - score_impact (weight: 35% / 0.35)
   - score_fit (weight: 25% / 0.25)
   - score_feasibility (weight: 20% / 0.20)
   - score_learning_speed (weight: 10% / 0.10)
   - score_cost_efficiency (weight: 10% / 0.10)
   Tip: Choose clean round numbers (multiples of 10 or 20 like 80, 70, 60) for sub-scores so arithmetic is exact.
5. Calculate priority_score with strict mathematical accuracy:
   priority_score = round((0.35 * score_impact) + (0.25 * score_fit) + (0.20 * score_feasibility) + (0.10 * score_learning_speed) + (0.10 * score_cost_efficiency), 2)
   CRITICAL: priority_score MUST strictly match this formula. Verify your arithmetic before outputting.
6. Select exactly three channels.
7. Design a repeatable system for each selected channel.
8. Build a four-week execution roadmap.
9. Assign an owner, deadline (due_day 1-30), success metric, and deliverable to every task.
10. Check budgets, dependencies, assumptions, schema requirements, and business constraints before returning the report.
