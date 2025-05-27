from django.db import models
from django.contrib.postgres.fields import ArrayField
from device_management.models import Device

class HarmonicAnalysis(models.Model):
    timestamp = models.DateTimeField(db_index=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    
    # Fundamental frequency component
    fundamental_voltage = models.FloatField()
    fundamental_current = models.FloatField()
    
    # Harmonic components (up to 63rd harmonic)
    voltage_harmonics = ArrayField(models.FloatField(), size=64)  # Magnitude
    current_harmonics = ArrayField(models.FloatField(), size=64)  # Magnitude
    voltage_phases = ArrayField(models.FloatField(), size=64)     # Phase angles
    current_phases = ArrayField(models.FloatField(), size=64)     # Phase angles
    
    # THD calculations
    voltage_thd = models.FloatField()
    current_thd = models.FloatField()
    
    # Individual harmonic percentages (most significant ones)
    h3_voltage = models.FloatField()
    h5_voltage = models.FloatField()
    h7_voltage = models.FloatField()
    h3_current = models.FloatField()
    h5_current = models.FloatField()
    h7_current = models.FloatField()
    
    class Meta:
        db_table = 'harmonic_analysis'
        indexes = [
            models.Index(fields=['timestamp', 'device']),
        ]
