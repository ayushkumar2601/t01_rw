from pydantic import BaseModel, Field, ConfigDict, StrictStr, StrictInt, StrictFloat
from typing import List, Union

class ExecutiveSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    company_name: StrictStr = Field(min_length=1)
    primary_bottleneck: StrictStr = Field(min_length=1)
    key_findings: List[StrictStr] = Field(min_length=1)
    strategic_thesis: StrictStr = Field(min_length=1)
    primary_30_day_objective: StrictStr = Field(min_length=1)
    assumptions: List[StrictStr]

class PrioritizedGrowthChannel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    rank: StrictInt = Field(ge=1, le=3)
    channel: StrictStr = Field(min_length=1)
    priority_score: Union[StrictInt, StrictFloat] = Field(ge=0, le=100)
    rationale: StrictStr = Field(min_length=1)
    supporting_evidence: List[StrictStr] = Field(min_length=1)
    system_to_build: StrictStr = Field(min_length=1)
    leading_kpi: StrictStr = Field(min_length=1)
    target: StrictStr = Field(min_length=1)
    budget_usd: Union[StrictInt, StrictFloat] = Field(ge=0)
    time_to_signal_days: StrictInt = Field(gt=0)
    risks: List[StrictStr]
    score_impact: StrictInt = Field(ge=0, le=100)
    score_fit: StrictInt = Field(ge=0, le=100)
    score_feasibility: StrictInt = Field(ge=0, le=100)
    score_learning_speed: StrictInt = Field(ge=0, le=100)
    score_cost_efficiency: StrictInt = Field(ge=0, le=100)

class Action(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    task: StrictStr = Field(min_length=1)
    owner: StrictStr = Field(min_length=1)
    due_day: StrictInt = Field(ge=1, le=30)
    success_metric: StrictStr = Field(min_length=1)
    deliverable: StrictStr = Field(min_length=1)

class WeeklyPhase(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    week: StrictInt = Field(ge=1, le=4)
    theme: StrictStr = Field(min_length=1)
    objective: StrictStr = Field(min_length=1)
    actions: List[Action]

class ReportSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    executive_summary: ExecutiveSummary
    prioritized_growth_channels: List[PrioritizedGrowthChannel] = Field(min_length=3, max_length=3)
    action_plan_30_days: List[WeeklyPhase] = Field(min_length=4, max_length=4)
