# Native imports 
import time
import random 
import logging
import calendar 
from tqdm import tqdm  # For progress bar
from typing import List
from datetime import datetime

# Custom-code imports 
from classes.brand import Brand 
from classes.campaign import Campaign 
from classes.ad_agency import AdAgency

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("ad_agency.log"), logging.StreamHandler()],
)
def setup_campaigns() -> List[Campaign]:
    """Create and return a list of Campaign objects."""
    return [
        Campaign(name="Campaign1", dayparting_schedule=[(9, 17)]),
        Campaign(name="Campaign2", dayparting_schedule=[(12, 20)]),
    ]

def setup_brands(campaigns: List[Campaign]) -> List[Brand]:
    """Create and return a list of Brand objects."""
    return [
        Brand(name="Brand1", daily_budget=1000, monthly_budget=30000, campaigns=campaigns),
        Brand(name="Brand2", daily_budget=1500, monthly_budget=45000, campaigns=[campaigns[0]]),
    ]

def simulate_month(agency: AdAgency):
    """Simulate an entire month of ad spending and campaign management."""
    now = datetime.now()
    month_name = now.strftime("%B")
    days_in_month = calendar.monthrange(now.year, now.month)[1]  # Get number of days in the month
    total_hours = days_in_month * 24  # Total hours in the month

    logging.info(f"Simulating {month_name} ({days_in_month} days)...")

    # Initialize progress bar
    with tqdm(total=total_hours, desc="Simulating hours", unit="hour") as pbar:
        for day in range(1, days_in_month + 1):
            pbar.set_description(f"Day {day}/{days_in_month}")  # Update progress bar description
            for hour in range(24):
                current_hour = hour  # Simulate each hour
                for brand in agency.brands:
                    # Simulate random spend
                    spend = random.uniform(0, brand.daily_budget / 10)
                    brand.update_spend(spend)
                    brand.check_budgets()

                    # Handle dayparting
                    for campaign in brand.campaigns:
                        if not campaign.is_active(current_hour):
                            campaign.status = False

                time.sleep(0.1)  # Simulate 1 hour in real time
                pbar.update(1)  # Update progress bar

            # Reset daily budget at the end of the day
            logging.info(f"Resetting daily budgets for Day {day}...")
            agency.reset_daily()

    # Reset monthly budget at the end of the month
    logging.info(f"Resetting monthly budgets for {month_name}...")
    agency.reset_monthly()

def main():
    """Main function to run the ad agency simulation."""
    try:
        logging.info("Starting ad agency simulation...")

        # Setup campaigns and brands
        campaigns = setup_campaigns()
        brands = setup_brands(campaigns)
        agency = AdAgency(brands=brands)

        # Simulate a full month
        simulate_month(agency)

        logging.info("Simulation completed successfully!")

    except Exception as e:
        logging.error(f"An error occurred during simulation: {e}")
    finally:
        logging.info("Ad agency simulation ended.")

if __name__ == "__main__":
    main()