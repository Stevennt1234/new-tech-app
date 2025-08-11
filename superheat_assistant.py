def calculate_superheat(suction_temp: float, saturation_temp: float) -> float:
    return round(suction_temp - saturation_temp, 2)
