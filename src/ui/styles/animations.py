from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor

class HudAnimations:
    """Motor de animações e efeitos visuais modernos para a HUD do Eco-Vida."""

    @staticmethod
    def apply_glow_shadow(widget, blur_radius=20, color=QColor(56, 161, 105, 120)):
        """Aplica um efeito de sombra luminosa (neon glow) nos componentes principais."""
        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(blur_radius)
        shadow.setColor(color)
        shadow.setOffset(0, 0)
        widget.setGraphicsEffect(shadow)
        return shadow

    @staticmethod
    def fade_in(widget, duration=400):
        """Aplica uma animação suave de fade-in no widget."""
        anim = QPropertyAnimation(widget, b"windowOpacity")
        anim.setDuration(duration)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()
        return anim