from django.db import models
from device_management.models import Device

class PowerQualityMetrics(models.Model):
    timestamp = models.DateTimeField(db_index=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    
    # Power measurements
    active_power = models.FloatField()  # Watts
    reactive_power = models.FloatField()  # VAR
    apparent_power = models.FloatField()  # VA
    power_factor = models.FloatField()
    
    # Voltage measurements
    voltage_rms = models.FloatField()
    voltage_thd = models.FloatField()  # Total Harmonic Distortion
    voltage_unbalance = models.FloatField(null=True, blank=True)  # For 3-phase
    
    # Current measurements
    current_rms = models.FloatField()
    current_thd = models.FloatField()
    current_unbalance = models.FloatField(null=True, blank=True)  # For 3-phase
    
    # Frequency
    frequency = models.FloatField()
    frequency_deviation = models.FloatField()
    
    # Efficiency metrics
    efficiency = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'power_quality_metrics'
        indexes = [
            models.Index(fields=['timestamp', 'device']),
            models.Index(fields=['device', 'timestamp']),
        ]
