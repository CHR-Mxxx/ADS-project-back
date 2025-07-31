def calculate_possible_scores(total_notes, target_score):
    """
    计算达到目标分数的所有可能性
    
    参数:
        total_notes: 谱面总物量(Note总数)
        target_score: 目标分数(0-1000000)
    
    返回:
        包含所有可能性的列表，每个可能性是一个字典，包含:
        - perfect: Perfect判定数量
        - good: Good判定数量
        - max_combo: 最大连击数
        - score: 实际分数
    """
    possibilities = []
    
    # 计算单个Note的判定分
    note_score = 900000 / total_notes
    
    # 遍历所有可能的Perfect和Good数量组合
    for perfect in range(total_notes + 1):
        for good in range(total_notes - perfect + 1):
            # 剩余的是Bad/Miss
            bad = total_notes - perfect - good
            
            # 计算判定分部分
            judgement_score = perfect * note_score + good * note_score * 0.65
            
            # 计算剩余的分数需要由连击分补足
            remaining_score = target_score - judgement_score
            
            # 如果剩余分数为0，连击分可以是任意值(不影响总分)
            if remaining_score == 0:
                # 可以有任何连击数，但通常至少是1
                for combo in range(1, total_notes + 1):
                    possibilities.append({
                        'perfect': perfect,
                        'good': good,
                        'bad': bad,
                        'max_combo': combo,
                        'score': target_score
                    })
                continue
            
            # 检查剩余分数是否在连击分可能范围内
            if remaining_score < 0 or remaining_score > 100000:
                continue
            
            # 计算需要的连击数
            required_combo_ratio = remaining_score / 100000
            required_combo = round(required_combo_ratio * total_notes)
            
            # 由于四舍五入，需要验证这个连击数是否真的能得到目标分数
            actual_combo_score = round(required_combo / total_notes * 100000)
            
            if abs((judgement_score + actual_combo_score) - target_score) < 1:  # 允许微小浮点误差
                possibilities.append({
                    'perfect': perfect,
                    'good': good,
                    'bad': bad,
                    'max_combo': required_combo,
                    'score': judgement_score + actual_combo_score
                })
    
    return possibilities