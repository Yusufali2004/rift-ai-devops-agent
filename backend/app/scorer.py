import time

def calculate_final_score(start_time, end_time, total_commits, base_score=100):
    """
    Calculates the final RIFT performance score based on speed and efficiency.
    Returns a dictionary with the final score and a breakdown of bonuses/penalties.
    """
    # 1. Calculate time duration
    total_duration_seconds = end_time - start_time
    duration_minutes = total_duration_seconds / 60
    
    score = base_score
    speed_bonus = 0
    efficiency_penalty = 0
    
    # 2. Speed Bonus: +10 if completed in less than 5 minutes (300 seconds)
    if duration_minutes < 5:
        speed_bonus = 10
        score += speed_bonus
        
    # 3. Efficiency Penalty: -2 per commit over 20
    # Higher commit counts suggest the agent is "guessing" rather than "reasoning."
    if total_commits > 20:
        penalty_units = total_commits - 20
        efficiency_penalty = penalty_units * 2
        score -= efficiency_penalty
        
    # 4. Final Score Floor (Ensure it doesn't go negative)
    final_score = max(score, 0)

    # Return structured data for the React Scoreboard
    return {
        "final_score": final_score,
        "breakdown": {
            "base_score": base_score,
            "speed_bonus": speed_bonus,
            "efficiency_penalty": -efficiency_penalty,
            "total_time_seconds": round(total_duration_seconds, 2),
            "total_commits": total_commits
        }
    }