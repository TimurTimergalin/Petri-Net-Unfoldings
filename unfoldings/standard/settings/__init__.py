from .configurations import BasicConfigurationSettings, FoataConfigurationSettings, LengthSettings
from .cutoff_detection import BasicCutoffDetection
from .abstract import Settings, Configuration


class McMillanSettings(BasicConfigurationSettings, BasicCutoffDetection):
    pass


class ErvSettings(FoataConfigurationSettings, BasicCutoffDetection):
    pass


__all__  = [
    "McMillanSettings",
    "ErvSettings",
    "Settings",
    "Configuration",
    "LengthSettings"
]
