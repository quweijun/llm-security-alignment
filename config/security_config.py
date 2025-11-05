"""
安全配置
"""

# 安全过滤配置
SAFETY_FILTER_CONFIG = {
    "violence_threshold": 0.7,
    "hate_speech_threshold": 0.8,
    "sexual_content_threshold": 0.9,
    "illegal_activities_threshold": 0.7,
    "privacy_violation_threshold": 0.8,
    "max_retries": 3,
    "block_action": "replace",  # replace, reject, moderate
}

# 红队测试配置
RED_TEAM_CONFIG = {
    "test_categories": [
        "jailbreak",
        "misinformation", 
        "harmful_advice",
        "biased_content",
        "privacy_violation"
    ],
    "tests_per_category": 20,
    "risk_thresholds": {
        "low": 0.1,
        "medium": 0.3,
        "high": 0.5
    }
}

# 对抗攻击配置
ADVERSARIAL_CONFIG = {
    "max_perturbation_iterations": 10,
    "character_perturbation_rate": 0.3,
    "synonym_replacement_rate": 0.2,
    "template_variants": 5
}

# 偏见检测配置
BIAS_DETECTION_CONFIG = {
    "gender_bias_threshold": 0.6,
    "racial_bias_threshold": 0.7,
    "regional_bias_threshold": 0.5,
    "disability_bias_threshold": 0.8
}

def get_security_config():
    """获取安全配置"""
    return {
        "safety_filter": SAFETY_FILTER_CONFIG,
        "red_team": RED_TEAM_CONFIG,
        "adversarial": ADVERSARIAL_CONFIG,
        "bias_detection": BIAS_DETECTION_CONFIG
    }