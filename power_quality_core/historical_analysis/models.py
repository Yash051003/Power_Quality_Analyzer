from django.db import models
from device_management.models import Device

class DailyReport(models.Model):
    date = models.DateField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    
    # Summary statistics
    avg_voltage = models.FloatField()
    max_voltage = models.FloatField()
    min_voltage = models.FloatField()
    avg_current = models.FloatField()
    max_current = models.FloatField()
    avg_power_factor = models.FloatField()
    avg_frequency = models.FloatField()
    
    # Power quality metrics
    avg_voltage_thd = models.FloatField()
    avg_current_thd = models.FloatField()
    max_voltage_thd = models.FloatField()
    max_current_thd = models.FloatField()
    
    # Energy consumption
    total_energy_consumed = models.FloatField()  # kWh
    peak_demand = models.FloatField()  # kW
    
    # Event counts
    voltage_sag_count = models.IntegerField(default=0)
    voltage_swell_count = models.IntegerField(default=0)
    interruption_count = models.IntegerField(default=0)
    high_thd_count = models.IntegerField(default=0)
    
    # Uptime
    uptime_percentage = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'daily_reports'
        unique_together = ['date', 'device']
        ordering = ['-date']


class TrendAnalysis(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Trend metrics
    trend_direction = models.CharField(max_length=20)  # 'increasing', 'decreasing', 'stable'
    trend_slope = models.FloatField()
    correlation_coefficient = models.FloatField()
    
    # Statistical data
    mean_value = models.FloatField()
    std_deviation = models.FloatField()
    min_value = models.FloatField()
    max_value = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'trend_analysis'