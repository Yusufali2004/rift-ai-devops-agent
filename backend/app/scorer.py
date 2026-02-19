import time

def calculate_final_score(start_time, end_time, total_commits, base_score=100):
    duration_minutes = (end_time - start_time) / 60
    
    score = base_score
    
    # Speed Bonus: +10 if < 5 minutes
    if duration_minutes < 5:
        score += 10
        
    # Efficiency Penalty: -2 per commit over 20
    if total_commits > 20:
        penalty = (total_commits - 20) * 2
        score -= penalty
        
    return max(score, 0)