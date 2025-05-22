from .flyoutdocks import FlyoutDocksPlugin

def classFactory(iface):
    return FlyoutDocksPlugin(iface)
