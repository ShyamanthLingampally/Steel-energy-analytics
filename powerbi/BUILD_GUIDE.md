# Power BI Dashboard

A 3-page Power BI dashboard built on top of the cleaned dataset produced by the Python pipeline (`energy_clean.csv`). Pages cover executive summary, load and cost analysis, and design/publish notes.

---

## Data Source

Power BI reads `energy_clean.csv` directly. Data types applied in Power Query:

- `date` — Date/Time
- `Usage_kWh`, `CO2tCO2`, power factor columns — Decimal Number
- `hour`, `month` — Whole Number

---

## DAX Measures

```dax
Total kWh = SUM(energy[Usage_kWh])

Avg kWh per Interval = AVERAGE(energy[Usage_kWh])

Total CO2 Tons = SUM(energy[CO2tCO2])

Estimated Cost = [Total kWh] * 0.10

% Intervals Below 90 PF =
DIVIDE(
    CALCULATE(COUNTROWS(energy), energy[Lagging_Current_Power_Factor] < 90),
    COUNTROWS(energy)
) * 100

Max Load % of Time =
DIVIDE(
    CALCULATE(COUNTROWS(energy), energy[Load_Type] = "Maximum Load"),
    COUNTROWS(energy)
) * 100

Max Load % of Energy =
DIVIDE(
    CALCULATE(SUM(energy[Usage_kWh]), energy[Load_Type] = "Maximum Load"),
    SUM(energy[Usage_kWh])
) * 100
```

---

## Page 1: Executive Summary

- Title: "Steel Plant Energy Performance — 2018"
- 4 KPI cards: Total kWh, Estimated Cost, Total CO2 Tons, % Below 90 PF
- Line chart: `hour` on X, `Avg kWh per Interval` on Y — "Daily Load Profile"
- Clustered column: `month` on X, `Total kWh` on Y — "Monthly Consumption"
- Donut chart: `Load_Type` with `Total kWh` — "Energy by Load Type"
- Slicers: `Day_of_week`, `WeekStatus`, `month_name`

---

## Page 2: Load & Cost Analysis

- Matrix heatmap: Rows = `Day_of_week`, Columns = `hour`, Values = `Avg kWh per Interval` with conditional formatting
- Clustered bar: `Load_Type` compared against `Max Load % of Time` and `Max Load % of Energy`
- Card: Weekend baseload as % of weekday
- Scatter: `Lagging_Current_Power_Factor` vs `Usage_kWh` to surface inefficiency patterns

---

## Design Rules

- Red for problems (high usage, low PF), blue for baseline, green for savings
- Chart titles state the finding, not the metric
- White backgrounds, subtle borders
- Segoe UI 14pt bold for chart titles
