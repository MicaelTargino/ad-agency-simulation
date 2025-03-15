from typing import List, Tuple

from pydantic import BaseModel, field_validator

class Campaign(BaseModel):
    name: str
    dayparting_schedule: List[Tuple[int, int]]  #  [(start_hour, end_hour)...]
    status: bool = True

    @field_validator("name")
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("Campaign name cannot be empty")
        return value

    @field_validator("dayparting_schedule")
    def validate_dayparting_schedule(cls, value):
        for start, end in value:
            if not (0 <= start < 24 and 0 <= end <= 24):
                raise ValueError("Dayparting hours must be between 0 and 24")
            if start >= end:
                raise ValueError("Start hour must be before end hour")
        return value

    def is_active(self, current_hour: int) -> bool:
        """Returns whether the Campaign is *active* or *inactive*

        Logic:
            if current_hour is inside any interval of campaign activeness listed in dayparting_schedule,
                Return True 
            else
                return False
        Examples: 
            Given:  dayparting_schedule = [(2,4), (9,12)]
                    current_hour = 3
            Return:
                    True
            ------------
            Given: dayparting_schedule = [(1,3), (5,8)]
                   current_hour = 4
            Return:
                    False

        """
        return any(start <= current_hour < end for (start, end) in self.dayparting_schedule)