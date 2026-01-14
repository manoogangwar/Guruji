def calculate_category_and_priority(total_score, total_questions=5):
    if total_score >= total_questions:
        return "advanced", 100

    elif total_score >= total_questions * 0.6:
        return "intermediate", 60

    return "beginner", 30


def calculate_profile_completeness(user):
    score = 0

    contact = getattr(user, "contact_info", None)
    professional = getattr(user, "professional_info", None)

    if professional:
        if professional.occupation:
            score += 10
        if professional.education:
            score += 10

    if contact:
        if contact.city:
            score += 10
        if contact.country:
            score += 10

    return score


def calculate_activity_score(user):
    score = 0

    if user.last_login:
        score += 5

    return min(score, 20)


def calculate_total_score(user, survey_score):
    profile_score = calculate_profile_completeness(user)
    activity_score = calculate_activity_score(user)

    return survey_score + profile_score + activity_score


def calculate_final_rank(total_score):
    if total_score >= 100:
        return 1
    elif total_score >= 70:
        return 2
    elif total_score >= 40:
        return 3
    else:
        return 4
