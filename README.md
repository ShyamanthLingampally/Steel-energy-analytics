# Industrial Energy Consumption and Peak Load Analysis

## Executive Summary

This project analyzes 35,040 intervals of 15-minute energy consumption data from a real steel manufacturing plant (DAEWOO Steel Co. Ltd, Gwangyang, South Korea, 2018) to identify cost drivers, peak load patterns, and concrete peak-shaving opportunities. By examining energy usage across time-of-day, day-of-week, load type, and power factor dimensions, this analysis outlines a clear roadmap for reducing industrial energy costs, with projected savings of ~$4,300/year from demand charge reduction and a 33% power factor penalty exposure that represents meaningful additional savings once remediated.

**Key Insights:**

* **Peak Load Concentration:** Plant demand hits 14x the overnight baseline between hours 8-17, with a clear lunch-break dip at noon. Demand charges are driven entirely by this business-hours peak window.
* **Maximum Load Cost Driver:** Maximum Load operations account for only 21% of operating time but drive 45% of total energy consumption - a high-leverage target for peak shaving.
* **Weekend Dead Load:** Plant consumes 35% of weekday average on weekends when not actively producing, representing ~$11,700/year in potentially avoidable baseload.
* **Power Factor Penalty Exposure:** 55% of intervals run below the 90% power factor threshold that typically triggers utility demand penalties - a material efficiency issue addressable via capacitor banks.
* **Seasonal Maintenance Window:** September is the lowest-consumption month and the natural window for scheduled plant maintenance with minimal production impact.

**Impact:**
The analysis provides quantified recommendations for reducing industrial energy costs, with projected savings of ~$4,300/year from a 15% peak shaving program alone, plus additional savings from power factor correction. These are achievable through production scheduling changes and capacitor bank investment, not capital-intensive equipment replacement.

**Demonstrated Skills:**

* **Advanced Data Analysis:** Expertise in extracting actionable insights from time-series industrial data using Python (Pandas), SQL, and structured analytical frameworks.
* **Industrial Operations Thinking:** Ability to translate raw energy measurements into the operational concepts energy managers actually use - demand charges, peak shaving, power factor, load types.
* **Effective Communication:** Strong proficiency in presenting findings through clean visualizations and dollar-impact framing that aligns with business decision-making.

This project showcases the ability to take raw industrial sensor data and turn it into concrete operational recommendations, making it a directly applicable asset for supply chain, plant operations, and energy management roles.

## Table of Contents

* [Technologies Used](#technologies-used)
* [Data Source](#data-source)
* [Business Question](#business-question)
* [Methodology](#methodology)
* [Process](#process)
* [Business Question Insights and Recommendations](#business-question-insights-and-recommendations)
* [Stakeholder Recommended Next Steps](#stakeholder-recommended-next-steps)
  + [High Priority](#high-priority)
  + [Medium Priority](#medium-priority)
  + [Low Priority](#low-priority)
* [Recommendations for Further Analysis](#recommendations-for-further-analysis)
* [Estimated Impact of Proposed Actions](#estimated-impact-of-proposed-actions)
* [Conclusion](#conclusion)
* [Contact](#contact)

## Technologies Used

* **Anaconda Prompt:** Environment management and package installation.
* **Python (Version 3.11+):** Core programming language for data analysis, with the following libraries:
  + **Pandas:** Data cleaning and manipulation.
  + **Numpy:** Numerical operations and data manipulation.
  + **Matplotlib:** Data visualization and chart generation.
* **SQL (SQLite):** Query layer for reusable time-of-use analysis, load classification, and efficiency benchmarking.
* **Power BI Desktop:** Interactive dashboard with executive summary, load analysis, and power factor efficiency views.
* **UCI Machine Learning Repository:** Source of the Steel Industry Energy Consumption dataset.
* **Git:** Version control for tracking changes and managing project history, with deployment to GitHub.

## Data Source

[This](https://archive.ics.uci.edu/dataset/851/steel+industry+energy+consumption) dataset contains real 15-minute interval energy consumption records from DAEWOO Steel Co. Ltd, a steel manufacturer in Gwangyang, South Korea, collected via the Korea Electric Power Corporation (KEPCO) and published in a 2021 academic paper by Sathishkumar et al. in Building Research & Information. The dataset includes columns such as timestamp, Usage_kWh, reactive power (lagging/leading), CO2 emissions, power factor (lagging/leading), day of week, week status, and load type classification. 35,040 observations cover the full year 2018.

* **DOI:** 10.24432/C52G8C
* **License:** Creative Commons Attribution 4.0

## Business Question

**"Where is peak load concentrated across the plant's operating year, and what peak shaving or efficiency opportunities could reduce industrial energy costs without capital investment?"**

## Methodology

This project conducts a detailed time-of-use and load-type analysis of a full year of industrial energy consumption data, segmented across hour-of-day, day-of-week, load classification, and power factor dimensions. Time-series segmentation enables operational managers to distinguish between structural energy costs (baseload) and controllable energy costs (peak demand), which are treated very differently by utility rate structures.

**Time-of-use analysis** is employed as it directly maps to how industrial energy bills are structured. Utilities charge both a per-kWh consumption rate and a separate demand charge tied to the plant's peak 15-minute demand in each billing cycle. This means the timing of consumption matters as much as the volume, and peak-shaving through scheduling changes can reduce demand charges without reducing total production.

The analysis focuses on the following key metrics:

* **Peak-to-Off-Peak Ratio:** Measures how much bigger peak hour consumption is versus the overnight baseline, indicating the headroom for peak shaving.
* **Load Type Distribution:** Compares the percentage of time spent in each load classification (Light/Medium/Maximum) vs the percentage of total energy consumed, identifying where intervention has highest leverage.
* **Weekend vs Weekday Baseload Ratio:** Quantifies the non-productive energy consumption outside operating hours as a percentage of productive consumption.
* **Power Factor Compliance:** Tracks the percentage of intervals where lagging power factor drops below 90% - the threshold that typically triggers utility demand penalties on industrial contracts.

## Process

1. **Data and Libraries Import and Loading:** Imported necessary Python libraries including pandas, numpy, and matplotlib. Loaded the UCI Steel Industry Energy Consumption dataset from the raw CSV, ensuring latin-1 encoding and DD/MM/YYYY date parsing were handled correctly.
2. **Data Cleaning and Transformation:** Standardized column names (removed dots, parentheses), parsed date columns, extracted derived time components (hour, month, month name, day number), and standardized categorical labels (Load_Type values).
3. **Exploratory Data Analysis (EDA):** Conducted initial exploration of the dataset to understand consumption patterns by hour, day-of-week, and load type. Verified data quality and checked for gaps in the 15-minute interval coverage.
4. **SQL Database Build:** Loaded the cleaned dataset into SQLite to enable a reusable SQL query layer covering annual footprint, peak hours, weekday vs weekend, load type breakdown, power factor efficiency, monthly patterns, and hourly heatmap data.
5. **Time-of-Use Analysis:** Calculated average and total energy consumption by hour of day to identify peak concentration windows and quantify peak-to-off-peak multiples.
6. **Load Type Analysis:** Segmented intervals by load classification and compared time-weighted vs energy-weighted distributions to identify the high-leverage cost driver.
7. **Weekend Baseload Analysis:** Compared weekday vs weekend consumption patterns to quantify non-productive baseload.
8. **Power Factor Efficiency Assessment:** Calculated the percentage of intervals running below the 90% power factor threshold to estimate utility penalty exposure.
9. **Seasonal Pattern Analysis:** Aggregated consumption by month to identify natural maintenance windows and peak demand periods.
10. **Peak-Shaving Opportunity Modeling:** Estimated potential savings from shifting 15% of Maximum Load consumption to off-peak windows, using industry-standard assumptions for demand charge portion of industrial utility bills.
11. **Visualization and Dashboard Build:** Created four summary charts for README documentation and provided a Power BI build guide for an interactive three-page dashboard (executive summary, load analysis, power factor efficiency).

## Business Question Insights and Recommendations

1. **Peak Load is Highly Concentrated and Actionable:**

* **Observation:** Average hourly usage hits 59 kWh at 9am versus just 4 kWh overnight - a 14x peak-to-off-peak multiple. The peak window is tightly clustered between hours 8-17 with a clear lunch-break dip at noon. This concentration means demand charges are driven by a predictable, narrow operating window.
* **Recommendation:** Production scheduling interventions should focus specifically on the 9-11am peak. Shifting preheat cycles, battery charging, or non-critical auxiliary loads to overnight windows would directly reduce the billed demand peak without impacting production throughput.

2. **Maximum Load Drives Disproportionate Energy Cost:**

* **Observation:** Maximum Load periods occupy only 21% of operating time but account for 45% of total energy consumption. This asymmetry means a small reduction in Maximum Load frequency has an outsized impact on total energy cost.
* **Recommendation:** Target Maximum Load duration first. A 15% reduction in Maximum Load intervals (achieved by staggering furnace runs or spreading high-draw operations) would yield an estimated $4,300/year in demand charge reduction alone - without reducing plant output.

3. **Weekend Baseload Represents Avoidable Waste:**

* **Observation:** The plant runs at 35% of weekday average on weekends, consuming approximately $11,700/year in energy during periods when active production is minimal. This baseload likely reflects HVAC, idle compressor air systems, and overnight heating equipment left running.
* **Recommendation:** Conduct an equipment audit on weekend baseload contributors. Even a partial reduction - turning off auxiliary systems when not in use - could cut weekend consumption by 30-50%. This is low-complexity operational work with direct cost savings and no capital requirement.

4. **Power Factor Exposure is a Material Hidden Cost:**

* **Observation:** 55% of intervals run with lagging power factor below 90%, the threshold at which most industrial utility contracts apply demand penalties. This exposure is structural (inductive machinery) and continuous (not incident-based).
* **Recommendation:** A power factor correction investment (typically capacitor banks at the service entrance) has a well-understood ROI in industrial settings. Even a 10-15 percentage point improvement in average power factor would eliminate the majority of penalty exposure and would typically pay back within 18-24 months.

5. **Seasonal Pattern Enables Better Maintenance Planning:**

* **Observation:** September is the lowest-consumption month of the year, while January is the highest (likely driven by Korean winter heating needs). This seasonal rhythm is predictable and stable.
* **Recommendation:** Schedule planned maintenance and equipment replacement activities in September to minimize production disruption and energy penalty exposure. Avoid maintenance activities in January when demand headroom is tightest.

## Stakeholder Recommended Next Steps

### High Priority

**Implement 15% Peak Shaving Program**

* **Action:** Reduce Maximum Load consumption during the 8-11am peak window by 15% through production scheduling changes.
* **Specific Steps:**
  + Identify which Maximum Load activities can be shifted to off-peak windows without production impact.
  + Stagger high-draw operations across multiple shifts to flatten the demand peak.
  + Track peak demand weekly against baseline and adjust scheduling as needed.

**Conduct Weekend Baseload Audit**

* **Action:** Identify and eliminate non-essential weekend energy consumption.
* **Specific Steps:**
  + Map all equipment running during weekend intervals to identify what's consuming the baseload.
  + Implement automated weekend shutdown procedures for HVAC, compressors, and auxiliary systems not needed for continuous operations.
  + Measure baseload reduction month over month.

### Medium Priority

**Deploy Power Factor Correction**

* **Action:** Install capacitor banks to reduce power factor penalty exposure.
* **Specific Steps:**
  + Commission a power quality study to size capacitor requirements.
  + Install capacitor banks at the service entrance to target 95%+ average power factor.
  + Verify penalty elimination on monthly utility bills.

### Low Priority

**Align Maintenance Windows with Low-Demand Months**

* **Action:** Reschedule planned maintenance to September each year.
* **Specific Steps:**
  + Build September maintenance into the annual operations calendar.
  + Avoid scheduling major equipment work in high-demand months (January in particular).
  + Use low-demand months for capital project tie-ins requiring partial shutdowns.

## Recommendations for Further Analysis

To further refine insights and enhance actionable outcomes, consider pursuing the following steps:

1. **Production Output Correlation:**

* Integrate production tonnage data with energy consumption to calculate kWh-per-ton efficiency.
* Identify which operations have the widest efficiency variance and target them for optimization.

2. **Real-Time Demand Monitoring:**

* Deploy real-time demand alerting to prevent new peak demand records mid-billing-cycle.
* Establish demand ceiling thresholds and automated shedding rules for non-critical loads.

3. **Weather and External Factor Analysis:**

* Incorporate weather data (temperature, heating degree days) to separate weather-driven demand from operational demand.
* Develop weather-normalized baselines for month-over-month comparability.

4. **Utility Rate Structure Optimization:**

* Review current utility contract terms and compare against alternative rate structures (time-of-use rates, interruptible service).
* Model projected annual cost under each rate structure using the plant's actual load profile.

## Estimated Impact of Proposed Actions

* **Peak Demand Charge Reduction:** Estimated **$4,300/year** savings through 15% peak shaving during 8-11am window. *(Based on industry-standard assumption that demand charges represent ~30% of industrial utility bills)*
* **Weekend Baseload Elimination:** Estimated **$3,000-$5,000/year** savings from partial weekend baseload reduction. *(Based on 30-50% reduction of current $11,700/year weekend consumption)*
* **Power Factor Penalty Elimination:** Typically **18-24 month payback** on capacitor bank investment for plants with current PF below 90% in majority of intervals.

## Conclusion

This project demonstrates the ability to take real industrial time-series sensor data and translate it into quantified operational recommendations aligned with how plant managers actually make decisions. By analyzing energy consumption through time-of-use, load type, and power factor dimensions, I identified concrete peak-shaving opportunities and power factor efficiency gains with projected savings of $4,300/year from scheduling changes alone and additional savings from weekend baseload reduction and power factor correction.

Key takeaways include:

* **Strategic Insight:** The analysis provided clear, data-driven recommendations that align with how industrial energy costs actually work, focusing on both immediate scheduling changes and longer-term efficiency investments.
* **Analytical Expertise:** Demonstrated proficiency in time-series analysis, SQL query design, and dashboard communication using real industrial sensor data at the 15-minute interval grain.
* **Effective Communication:** Successfully translated raw kWh measurements into the operational vocabulary (demand charges, peak shaving, power factor, load classification) that energy managers and plant operations teams use daily.

This project exemplifies my commitment to driving business value through data analysis, strategic thinking, and effective communication in the supply chain and operations domain. I am eager to bring these skills to a dynamic team where I can continue to contribute to data-driven operational excellence.

## Contact

For more information, please contact:

**Name:** Shyamanth Lingampally

**Email:** Shyamanthlingampally3@gmail.com

**LinkedIn:** [linkedin.com/in/shyamanth19a02](https://linkedin.com/in/shyamanth19a02)
