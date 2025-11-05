"""
提示词工具函数
"""

import re
from typing import List, Dict, Any

def sanitize_prompt(prompt: str) -> str:
    """清理提示词"""
    # 移除潜在的恶意字符
    malicious_patterns = [
        r'ignore.*previous',
        r'forget.*you.*are',
        r'developer.*mode',
        r'DAN.*mode',
        r'role.*play.*no.*restrictions'
    ]
    
    for pattern in malicious_patterns:
        prompt = re.sub(pattern, '', prompt, flags=re.IGNORECASE)
    
    # 移除多余空白
    prompt = re.sub(r'\s+', ' ', prompt).strip()
    
    return prompt

def detect_prompt_injection(prompt: str) -> Dict[str, Any]:
    """检测提示词注入"""
    injection_indicators = {
        'jailbreak_attempt': [
            r'忽略.*指令', r'忘记.*身份', r'开发者模式',
            r'无限制', r'角色扮演.*无约束'
        ],
        'system_prompt_leak': [
            r'系统提示', r'初始指令', r'你的设定',
            r'扮演.*角色'
        ],
        'instruction_override': [
            r'重新定义', r'覆盖指令', r'新的规则',
            r'从现在开始'
        ]
    }
    
    results = {
        'is_injection': False,
        'injection_types': [],
        'confidence': 0.0
    }
    
    detected_types = []
    for injection_type, patterns in injection_indicators.items():
        for pattern in patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                if injection_type not in detected_types:
                    detected_types.append(injection_type)
    
    if detected_types:
        results.update({
            'is_injection': True,
            'injection_types': detected_types,
            'confidence': min(1.0, len(detected_types) * 0.3)
        })
    
    return results

def create_safety_prompt(base_prompt: str, safety_instructions: str = None) -> str:
    """创建安全提示词"""
    if safety_instructions is None:
        safety_instructions = """
请确保你的回答:
1. 不包含有害、非法或不道德的内容
2. 尊重所有人的尊严和权利
3. 保护个人隐私和数据安全
4. 避免偏见和歧视性内容
5. 不传播虚假或误导性信息
"""
    
    return f"{safety_instructions}\n\n用户问题: {base_prompt}"