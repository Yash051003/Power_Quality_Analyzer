from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from device_management.views import DeviceViewSet
from signal_acquisition.views import RawMeasurementViewSet
from power_metrics.views import PowerQualityMetricsViewSet
from harmonic_analysis.views import HarmonicAnalysisViewSet
from notifications.views import PowerQualityEventViewSet, AlertRuleViewSet
from historical_analysis.views import DailyReportViewSet, DashboardAPIView

router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'measurements', RawMeasurementViewSet)
router.register(r'power-metrics', PowerQualityMetricsViewSet)
router.register(r'harmonics', HarmonicAnalysisViewSet)
router.register(r'events', PowerQualityEventViewSet)
router.register(r'alert-rules', AlertRuleViewSet)
router.register(r'reports', DailyReportViewSet)

# Schema configuration
schema_view = get_schema_view(
    title="Power Quality Analyzer API",
    description="API endpoints for power quality monitoring and analysis",
    version="1.0.0"
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/dashboard/', DashboardAPIView.as_view(), name='dashboard'),
    path('api-auth/', include('rest_framework.urls')),
    # DRF documentation and schema endpoints
    path('api/docs/', include_docs_urls(title='Power Quality Analyzer API')),
    path('api/schema/', schema_view, name='openapi-schema'),
] 