"""
对齐配置
"""

# 价值观对齐配置
VALUE_ALIGNMENT_CONFIG = {
    "core_values": [
        "诚实正直",
        "尊重他人", 
        "社会责任",
        "公平公正",
        "保护隐私",
        "促进福祉"
    ],
    "alignment_methods": [
        "constitutional_ai",
        "value_learning", 
        "reinforcement_learning",
        "supervised_finetuning"
    ],
    "safety_priority": "high"
}

# 安全微调配置
SAFETY_FINETUNE_CONFIG = {
    "learning_rate": 5e-5,
    "num_epochs": 3,
    "batch_size": 4,
    "warmup_steps": 100,
    "contrastive_learning": True,
    "constitutional_feedback": True
}

# RLHF配置
RLHF_CONFIG = {
    "reward_model_path": "models/reward_model",
    "kl_penalty": 0.1,
    "entropy_bonus": 0.01,
    "clip_range": 0.2,
    "value_clip": 0.2
}

# 输出安全配置
OUTPUT_SAFETY_CONFIG = {
    "real_time_monitoring": True,
    "conversation_history_depth": 5,
    "risk_escalation_threshold": 0.7,
    "auto_termination": True
}

def get_alignment_config():
    """获取对齐配置"""
    return {
        "value_alignment": VALUE_ALIGNMENT_CONFIG,
        "safety_finetune": SAFETY_FINETUNE_CONFIG,
        "rlhf": RLHF_CONFIG,
        "output_safety": OUTPUT_SAFETY_CONFIG
    }