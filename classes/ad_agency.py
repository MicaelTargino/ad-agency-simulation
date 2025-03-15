
# Native imports 
import random 
from typing import List 
from datetime import datetime 

# Lib imports
from pydantic import BaseModel, field_validator

# Local imports 
from .brand import Brand

class AdAgency(BaseModel):
    brands: List[Brand]

    @field_validator("brands")
    def validate_brands(cls, value):
        if not value:
            raise ValueError("AdAgency must have at least one brand")
        return value

    def simulate_day(self):
        current_hour = datetime.now().hour
        for brand in self.brands:
            # Simulate random spend
            spend = random.uniform(0, brand.daily_budget / 10)
            brand.update_spend(spend)
            brand.check_budgets()

            # Handle dayparting
            for campaign in brand.campaigns:
                if not campaign.is_active(current_hour):
                    campaign.status = False

    def reset_daily(self):
        for brand in self.brands:
            brand.reset_daily()

    def reset_monthly(self):
        for brand in self.brands:
            brand.reset_monthly()