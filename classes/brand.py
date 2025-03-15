from typing import List 

from pydantic import BaseModel, field_validator

from .campaign import Campaign

class Brand(BaseModel):
    name: str
    daily_budget: float
    monthly_budget: float
    daily_spend: float = 0.0
    monthly_spend: float = 0.0
    campaigns: List[Campaign] = []

    @field_validator("name")
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Brand name cannot be empty")
        return value

    @field_validator("daily_budget", "monthly_budget")
    def validate_budgets(cls, value):
        if value < 0:
            raise ValueError("Budget cannot be negative")
        return value

    @field_validator("campaigns")
    def validate_campaigns(cls, value):
        if not value:
            raise ValueError("Brand must have at least one campaign")
        return value

    def update_spend(self, amount: float):
        self.daily_spend += amount
        self.monthly_spend += amount

    def check_budgets(self):
        # If daily or monthly budget was reached, immediately deactivate all Campaigns of this Brand.

        print(f"\n{'=' * 40}")
        print(f"Brand: {self.name}")
        print(f"{'-' * 40}")
        print(f"Daily Spend: {self.daily_spend:.2f} / {self.daily_budget:.2f}")
        print(f"Monthly Spend: {self.monthly_spend:.2f} / {self.monthly_budget:.2f}")
        print(f"{'-' * 40}")

        if self.daily_spend >= self.daily_budget or self.monthly_spend >= self.monthly_budget:
            print(f"🚨 Brand {self.name} budget reached! Deactivating campaigns... 🚨")
            for campaign in self.campaigns:
                campaign.status = False
        else:
            print(f"✅ Brand {self.name} is within budget. Campaigns are active. ✅")
        print(f"{'=' * 40}\n")
    
    def reset_daily(self):
        self.daily_spend = 0 
    
    def reset_monthly(self):
        self.daily_spend = 0
        self.monthly_spend = 0