"""Experience matcher."""

from typing import (
    Optional,
)


class ExperienceMatcher:
    """Match resume experience against vacancy experience requirements."""

    def __init__(self):
        self.high_experience = False
        self.low_experience = False

    def calculate_experience(
        self,
        vacancy_expirience_min: Optional[float],
        vacancy_expirience_max: Optional[float],
        resume_expirience: float,
    ) -> None:
        """Determine whether resume experience meets vacancy requirements."""

        if vacancy_expirience_min and vacancy_expirience_max:
            # resume_expirience hight expirience
            if resume_expirience > float(vacancy_expirience_max):
                self.high_experience = True
            # resume_expirience low expirience
            elif float(vacancy_expirience_min) > resume_expirience:
                self.low_experience = True

        elif vacancy_expirience_min and not vacancy_expirience_max:
            # resume_expirience low expirience
            if float(vacancy_expirience_min) > resume_expirience:
                self.low_experience = True
