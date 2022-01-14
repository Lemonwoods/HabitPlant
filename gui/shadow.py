from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


def get_shadow_effect(parent):
    shadow_effect = QGraphicsDropShadowEffect(parent)
    shadow_effect.setOffset(8,8)
    shadow_effect.setBlurRadius(30)
    shadow_effect.setColor(QColor(0,0,0,70))
    return shadow_effect