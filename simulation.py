# Native imports 
import random
import time 
from typing import List, Dict, Tuple 
from datetime import datetime 
# Lib imports 
from pydantic import BaseModel, field_validator

class Campaign(BaseModel):
    name: str
    dayparting_schedule: List[Tuple[int, int]]  #  [(start_hour, end_hour)...]
    status: bool = True

    def is_active(self, current_hour: int) -> bool:
        """Returns whether the Campaign is *active* or *inactive*

        Logic:
            if current_hour is inside any interval of campaign activeness listed in dayparting_schedule,
                Return True 
            else
                return False
        Examples: 
            Given:  dayparting_schedule = [(2,4), (9,12)]
                    current_hour = 3
            Return:
                    True
            ------------
            Given: dayparting_schedule = [(1,3), (5,8)]
                   current_hour = 4
            Return:
                    False

        """
        return any(start <= current_hour < end for (start, end) in self.dayparting_schedule)

class Brand(BaseModel):
    name: str
    daily_budget: float
    monthly_budget: float
    daily_spend: float = 0.0
    monthly_spend: float = 0.0
    campaigns: List[Campaign] = []

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
        self.daily_spend = 0.0
        for campaign in self.campaigns:
            campaign.status = True

    def reset_monthly(self):
        self.monthly_spend = 0.0
        self.reset_daily()

class AdAgency(BaseModel):
    brands: List[Brand]

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

