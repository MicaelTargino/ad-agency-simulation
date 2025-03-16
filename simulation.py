# Native imports 
import time
import random 
import logging
import calendar 
from tqdm import tqdm  # For progress bar
from typing import List, Dict
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
    brand1_campaigns = [
        Campaign(name="Campaign1", dayparting_schedule=[(8, 19)]),
        Campaign(name="Campaign2", dayparting_schedule=[(12, 22)])
    ]
    brand2_campaigns = [
        Campaign(name="Campaign3", dayparting_schedule=[(13, 21)]),
        Campaign(name="Campaign4", dayparting_schedule=[(5, 12)])
    ]
    return {
        "brand1_campaigns": brand1_campaigns,
        "brand2_campaigns": brand2_campaigns
    }


def setup_brands(campaigns: Dict[str, List[Campaign]]) -> List[Brand]:
    """Create and return a list of Brand objects."""
    return [
        Brand(name="Brand1", daily_budget=1000, monthly_budget=30000, campaigns=campaigns.get("brand1_campaigns")),
        Brand(name="Brand2", daily_budget=1500, monthly_budget=45000, campaigns=campaigns.get("brand2_campaigns"))
    ]

def simulate_month(agency: AdAgency):
    """Simulate an entire month of ad spending and campaign management."""
    now = datetime.now()
    month_name = now.strftime("%B")
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    total_hours = days_in_month * 24

    logging.info(f"Simulating {month_name} ({days_in_month} days)...")

    with tqdm(total=total_hours, desc="Simulating hours", unit="hour") as pbar:
        for day in range(1, days_in_month + 1):
            pbar.set_description(f"Day {day}/{days_in_month}")
            for hour in range(24):
                current_hour = hour
                formatted_hour = f"{current_hour:02d}:00"
                
                for brand in agency.brands:
                    print(f"\n📅 Day {day} {formatted_hour} | Brand: {brand.name}")
                    status_updates = []
                    
                    # Handle dayparting first
                    for campaign in brand.campaigns:
                        prev_status = campaign.status
                        new_status = campaign.is_active(current_hour)
                        campaign.status = new_status
                        
                        # Only show changes in status
                        if prev_status != new_status:
                            status_emoji = "🟢" if new_status else "🔴"
                            schedule = ", ".join([f"{s}-{e}" for (s,e) in campaign.dayparting_schedule])
                            status_updates.append(
                                f"  {status_emoji} Campaign: {campaign.name} "
                                f"| Status: {'ACTIVE' if new_status else 'INACTIVE'} "
                                f"| Schedule: {schedule}"
                            )
                    
                    # Print dayparting status changes
                    if status_updates:
                        print("\n".join(status_updates))
                    else:
                        print("  🔄 No dayparting status changes")
                    
                    # Original spend/budget logic remains unchanged below
                    if any(campaign.status for campaign in brand.campaigns):
                        spend = random.uniform(0, brand.daily_budget / 5)
                        brand.update_spend(spend)
                        brand.check_budgets()

                time.sleep(0.25)
                pbar.update(1)

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