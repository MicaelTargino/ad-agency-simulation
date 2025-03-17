# 📊 Advertising Budget Simulation System | Python + Pydantic + Docker

A digital advertising agency simulation for modeling campaign budgets, dayparting schedules, and real-time spend tracking. Built with:

- **Core Features**:  
  ▶️ Daily/monthly budget enforcement  
  🕒 Dayparting-aware campaign activation  
  🔄 Real-time simulation (1 simulated hour = 0.5s)  
  ✅ Pydantic data validation  
  🐳 Docker containerization  

- **Use Case**:  
  Simulate ad spend scenarios for agencies/brands to optimize budget allocation and campaign scheduling.

- **Tech Stack**:  
  `Python` | `Pydantic` | `Docker` | `TQDM`

## How to Run

### Prerequisites
- Python 3.8+
- Docker (optional)

### Running with Docker (Recommended)
```bash
# Build and run the simulation
docker-compose up --build

# For clean removal
docker-compose down
```

### Running Locally
```bash 
pip install -r requirements.txt 
python simulation.py
```

## Data Structures

### Campaign Class
- **Attributes**:
  - `name`: Campaign identifier (`str`)
  - `dayparting_schedule`: List of active hourly windows as tuples `[(start_hour, end_hour)]`
  - `status`: Current state (`bool`, `True` = active)
- **Methods**:
  - `is_active(current_hour)`: Checks if campaign should be active based on current hour
  - Validation: Ensures valid hour ranges and non-empty name

### Brand Class
- **Attributes**:
  - `name`: Brand identifier (`str`)
  - `daily_budget`: Max allowed daily spend (`float`)
  - `monthly_budget`: Max allowed monthly spend (`float`)
  - `daily_spend`: Current day's accumulated spend (`float`)
  - `monthly_spend`: Current month's accumulated spend (`float`)
  - `campaigns`: List of associated `Campaign` objects
- **Methods**:
  - `update_spend(amount)`: Adds to daily/monthly spends
  - `check_budgets()`: Deactivates campaigns if budgets exceeded
  - `reset_daily()`: Resets daily values and reactivates campaigns
  - `reset_monthly()`: Full monthly reset
  - Validation: Ensures non-negative budgets and valid names

### AdAgency Class
- **Attributes**:
  - `brands`: List of `Brand` objects to manage
- **Methods**:
  - `simulate_month()`: Coordinates full monthly simulation cycle
  - Validation: Requires at least one brand

## Program Flow

1. **Initialization Phase**  
   - Campaigns are created with defined dayparting schedules  
   - Brands are initialized with budgets and assigned campaigns  
   - AdAgency is configured with brand configurations  

2. **Monthly Simulation Loop**  
   For each day in the month:  
   ```plaintext
   a. Daily Reset
      - Reset all daily spends to 0
      - Reactivate all campaigns (subject to dayparting)
   
   b. Hourly Execution (24 cycles)
      1. Dayparting Update:
         - Check current hour against schedules
         - Update campaign statuses
      2. Spend Calculation:
         - Generate random spend for active campaigns
         - Update budget totals
      3. Budget Enforcement:
         - Deactivate campaigns if limits exceeded
      4. Progress Update:
         - Advance simulation clock (0.5s real time)
    ``` 

3. Monthly Cleanup
    - Reset monthly spends 
     
## Monitoring 

### Real-Time Indicators

   - 📊 Progress bar showing completed hours/total monthly hours 
   - 📅 Day counter (e.g. "Day 5/31") in progress bar 
   - 🎨 Color-coded statuses:
   ```plaintext 
    🟢 Active campaign
    🔴 Inactive campaign
    🔄 No status change
  ```

### Budget Tracking
- **Hourly Updates**  
  ```plaintext
  Daily Spend: [current_spend]/[daily_budget] (e.g., 950.00/1000.00)
  Monthly Spend: [current_spend]/[monthly_budget] (e.g., 28000.00/30000.00)
  ```
- **Threshold Alerts**
  ```plaintext
    🚨 Brand [BrandName] budget reached! Deactivating campaigns...
    ✅ Brand [BrandName] is within budget. Campaigns are active.  
  ```

### Logging 
- **Persistent Storage**
  ```plaintext
  All operations logged to: ad_agency.log
  ```
- **Console Visibility**
  ```plaintext
    2023-10-15 12:00:00 - INFO - Resetting daily budgets for Day 5...
    2023-10-15 12:00:00 - ERROR - Validation failed: budgets cannot be negative
  ```
- **Status Changes**
  ```plaintext
  📅 Day 5 09:00 | Brand: Brand1
    🟢 Campaign: Campaign1 | Status: ACTIVE | Schedule: 9-17
  ```
