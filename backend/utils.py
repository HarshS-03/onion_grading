def calculate_quality_metrics(moisture, sprouting, damage, doubles):
    m = float(moisture or 0)
    s = float(sprouting or 0)
    d = float(damage or 0)
    db = float(doubles or 0)

    moisture_penalty = (m - 14.0) * 4.0 if m > 14.0 else 0.0
    sprouting_penalty = s * 2.5
    damage_penalty = d * 1.5
    doubles_penalty = db * 1.0

    raw_score = 100.0 - (moisture_penalty + sprouting_penalty + damage_penalty + doubles_penalty)
    score = max(0, min(100, round(raw_score)))

    if score >= 85:
        status = 'CERTIFIED'
    elif score >= 70:
        status = 'STANDARD'
    elif score >= 50:
        status = 'CONDITIONAL'
    else:
        status = 'REJECTED'

    return score, status
