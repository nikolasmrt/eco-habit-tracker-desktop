from typing import List, Dict, Any
from repositories.habit_repository import HabitRepository

class ScoreService:
    """Serviço responsável por aplicar as regras de negócio de gamificação e cálculo do score sustentável."""

    # Pesos multiplicadores por categoria de impacto
    PESOS = {
        'água': 5.0,
        'energia': 4.0,
        'transporte': 3.0,
        'resíduos': 2.0
    }

    # Metas ou referências de consumo base para cálculo de economia/excesso
    REFERENCIAS = {
        'água': 150.0,
        'energia': 10.0,
        'transporte': 30.0,
        'resíduos': 2.0
    }

    @staticmethod
    def calculate_user_score(user_id: int) -> float:
        """
        Calcula a pontuação de sustentabilidade baseada no consumo agrupado por categoria.
        Fórmula:
          - Consumo < Referência: Recompensa proporcional ao peso e à economia gerada.
          - Consumo >= Referência: Penalização proporcional ao excesso de consumo.
        """
        records: List[Dict[str, Any]] = HabitRepository.get_user_records_grouped(user_id)

        if not records:
            return 0.0

        score = 0.0

        for row in records:
            categoria = str(row.get('categoria', '')).lower()
            quantidade = row.get('total')

            if quantidade is None:
                continue

            try:
                qtd_float = float(quantidade)
            except (ValueError, TypeError):
                continue

            if categoria in ScoreService.PESOS and categoria in ScoreService.REFERENCIAS:
                ref = ScoreService.REFERENCIAS[categoria]
                peso = ScoreService.PESOS[categoria]

                if qtd_float < ref:
                    economia = (ref - qtd_float) / ref
                    pontos = economia * 100 * peso
                    score += pontos
                else:
                    excesso = (qtd_float - ref) / ref
                    pontos = -excesso * 10 * peso
                    score += pontos

        return max(round(score, 2), 0.0)