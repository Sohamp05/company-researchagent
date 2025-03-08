from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union


class KeyMetrics(BaseModel):
    revenue: Optional[str] = Field(default=None, description="Annual Revenue")
    profit: Optional[str] = Field(default=None, description="Annual Profit")
    market_cap: Optional[str] = Field(default=None, description="Market Capitalization")


class Competitor(BaseModel):
    company_name: str = Field(description="Name of the competitor")
    summary: Optional[str] = Field(description="Brief summary of the competitor")
    key_metrics: Optional[KeyMetrics] = Field(description="Key financial metrics of the competitor")


class CompetitorList(BaseModel):
    competitors: List[Competitor]


class DomainInfo(BaseModel):
    summary: Optional[str] = Field(default=None, description="Summary of information in this domain")
    key_metrics: Optional[KeyMetrics] = Field(default=None, description="Key financial metrics")
    market_share: Optional[str] = Field(default=None, description="Market share of the company")
    market_trends: Optional[List[str]] = Field(default_factory=list, description="List of market trends")
    competitors: Optional[List[str]] = Field(default_factory=list, description="List of competitors mentioned in the domain")
    legal_issues: Optional[List[str]] = Field(default_factory=list, description="List of legal issues")
    regulatory_environment: Optional[str] = Field(default=None, description="Description of the regulatory environment")
    lobbying_activities: Optional[str] = Field(default=None, description="Description of lobbying activities")
    political_contributions: Optional[str] = Field(default=None, description="Description of political contributions")
    demographics: Optional[str] = Field(default=None, description="Description of audience demographics")
    sentiment: Optional[str] = Field(default=None, description="Audience sentiment towards the company")
    news_links: Optional[List[str]] = Field(default_factory=list, description="List of relevant news links")

    @classmethod
    def parse_value(cls, value: Union[str, List[str]]) -> Union[str, List[str], None]:
        if isinstance(value, str):
            if value == "NA":
                return None  # for string fields, return None
            return value  # Return the string as it is if not "NA"
        elif isinstance(value, list):
            # If the list contains "NA", convert it to an empty list
            if "NA" in value:
                return [item for item in value if item != "NA"]  # Remove "NA" values
            return value  # Return the list as it is
        return value  # For other cases, just return the value


class CompanyResearch(BaseModel):
    company_name: str = Field(description="Name of the company")
    exists: bool = Field(description="Whether the company exists")
    domains: Dict[str, DomainInfo] = Field(description="Information about the company in different domains")
    competitors: Optional[List[Competitor]] = Field(description="List of key competitors")
