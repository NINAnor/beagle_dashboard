"""
Configuration settings for the BEAGLE dashboard.
"""

# Application settings
APP_TITLE = "BEAGLE Monitoring Dashboard"

# Map settings
DEFAULT_ZOOM = 6
MAP_HEIGHT = 600
MAP_WIDTH = 1200

# Privacy protection settings
MIN_ZOOM_LEVEL = 3  # Minimum zoom level
DETAILED_MAP_MAX_ZOOM = 18  # Maximum zoom level for authorized users (full detail)

# Chart settings
HEATMAP_COLORSCALE = "Viridis"
MIN_HEATMAP_HEIGHT = 400
HEATMAP_ROW_HEIGHT = 25

# Cache settings
CACHE_TTL = 3600  # 1 hour

# Data source URLs
BASE_DATA_URL = "http://rclone:8081/data"

# Tab icons
TAB_ICONS = {"map": "🗺️", "status": "📊", "activity": "📈"}
