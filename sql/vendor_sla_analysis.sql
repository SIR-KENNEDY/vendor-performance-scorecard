-- Vendor SLA ranking with window functions (PostgreSQL)
SELECT
    vendor_id, vendor_name,
    COUNT(*) AS total_deliveries,
    ROUND(SUM(CASE WHEN actual_date<=scheduled_date THEN 1 ELSE 0 END)*100.0/COUNT(*),2) AS on_time_pct,
    ROUND(AVG(qty_delivered::float/NULLIF(qty_ordered,0))*100,2) AS avg_qty_accuracy,
    RANK() OVER (ORDER BY SUM(CASE WHEN actual_date<=scheduled_date THEN 1 ELSE 0 END)*1.0/COUNT(*) DESC) AS sla_rank,
    NTILE(4) OVER (ORDER BY SUM(CASE WHEN actual_date<=scheduled_date THEN 1 ELSE 0 END)*1.0/COUNT(*) DESC) AS quartile
FROM vendor_deliveries
GROUP BY vendor_id, vendor_name
ORDER BY sla_rank;
