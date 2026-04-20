-- Steel Industry Energy Analysis - SQL queries
-- Run against data/energy.db (built by scripts/build_db.py)


-- 1. Annual energy footprint
SELECT
    ROUND(SUM(Usage_kWh), 0)           AS total_kwh,
    ROUND(SUM(Usage_kWh) * 0.10, 0)    AS estimated_cost_usd,
    ROUND(SUM(CO2tCO2), 1)             AS total_co2_tons,
    COUNT(*)                           AS intervals
FROM energy;


-- 2. Peak hour identification
SELECT
    hour,
    ROUND(AVG(Usage_kWh), 1)  AS avg_kwh,
    ROUND(MAX(Usage_kWh), 1)  AS max_kwh
FROM energy
GROUP BY hour
ORDER BY avg_kwh DESC
LIMIT 5;


-- 3. Weekday vs weekend consumption
SELECT
    WeekStatus,
    ROUND(AVG(Usage_kWh), 1)   AS avg_kwh,
    ROUND(SUM(Usage_kWh), 0)   AS total_kwh,
    ROUND(SUM(Usage_kWh) * 0.10, 0) AS cost_usd
FROM energy
GROUP BY WeekStatus;


-- 4. Load type breakdown - where's the energy actually going?
SELECT
    Load_Type,
    COUNT(*)                                                    AS intervals,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM energy), 1)  AS pct_time,
    ROUND(SUM(Usage_kWh), 0)                                    AS total_kwh,
    ROUND(SUM(Usage_kWh) * 100.0 /
          (SELECT SUM(Usage_kWh) FROM energy), 1)               AS pct_energy
FROM energy
GROUP BY Load_Type
ORDER BY total_kwh DESC;


-- 5. Power factor efficiency - are we getting utility penalties?
-- Industrial PF below 90% typically triggers demand charges
SELECT
    COUNT(*)                                                     AS total_intervals,
    SUM(CASE WHEN Lagging_Current_Power_Factor < 90 THEN 1 ELSE 0 END) AS below_90_intervals,
    ROUND(SUM(CASE WHEN Lagging_Current_Power_Factor < 90 THEN 1 ELSE 0 END)
          * 100.0 / COUNT(*), 1)                                 AS pct_below_90,
    ROUND(AVG(Lagging_Current_Power_Factor), 1)                  AS avg_lagging_pf
FROM energy;


-- 6. Monthly pattern for maintenance planning
SELECT
    month,
    month_name,
    ROUND(SUM(Usage_kWh), 0)  AS total_kwh,
    ROUND(AVG(Usage_kWh), 1)  AS avg_kwh
FROM energy
GROUP BY month, month_name
ORDER BY month;


-- 7. Hourly load distribution by day of week (heat map data)
SELECT
    Day_of_week,
    hour,
    ROUND(AVG(Usage_kWh), 1) AS avg_kwh
FROM energy
GROUP BY Day_of_week, hour
ORDER BY
    CASE Day_of_week
        WHEN 'Monday' THEN 1 WHEN 'Tuesday' THEN 2 WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4 WHEN 'Friday' THEN 5 WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END,
    hour;


-- 8. Top 10 highest consumption intervals - outlier analysis
SELECT
    date,
    Usage_kWh,
    Load_Type,
    Day_of_week,
    hour
FROM energy
ORDER BY Usage_kWh DESC
LIMIT 10;
