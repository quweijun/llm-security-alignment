import re
from typing import List, Dict, Any
import torch.nn as nn

class SafetyFilter:
    """安全过滤器"""
    
    def __init__(self):
        self.harmful_patterns = {
            'violence': [
                r'杀[死伤]', r'伤害', r'攻击', r'武器', r'爆炸', 
                r'自[杀伤]', r'暴力', r'殴打', r'恐怖'
            ],
            'hate_speech': [
                r'歧视', r'仇恨', r'侮辱', r'贬低', r'排斥',
                r'劣等', r'垃圾', r'废物'
            ],
            'sexual_content': [
                r'性[交扰]', r'色情', r'淫秽', r'猥亵', r'强奸'
            ],
            'illegal_activities': [
                r'毒品', r'盗窃', r'抢劫', r'诈骗', r'黑客',
                r'非法', r'犯罪', r'违禁'
            ],
            'privacy_violation': [
                r'密码', r'账号', r'隐私', r'窃听', r'跟踪',
                r'监控', r'偷拍'
            ]
        }
        
        self.safe_responses = [
            "抱歉，我无法提供这个信息。",
            "这个问题涉及到不安全的内容，我不能回答。",
            "作为AI助手，我不能提供可能造成伤害的信息。",
            "请咨询相关专业人士获取帮助。",
            "这个问题不适合讨论。"
        ]
    
    def filter_response(self, text: str, threshold: float = 0.7) -> Dict[str, Any]:
        """过滤不安全内容"""
        results = {
            'is_safe': True,
            'risk_categories': [],
            'confidence': 0.0,
            'filtered_text': text,
            'action': 'allow'
        }
        
        detected_categories = []
        max_confidence = 0.0
        
        for category, patterns in self.harmful_patterns.items():
            category_score = self._calculate_category_score(text, patterns)
            
            if category_score > threshold:
                detected_categories.append(category)
                max_confidence = max(max_confidence, category_score)
        
        if detected_categories:
            results.update({
                'is_safe': False,
                'risk_categories': detected_categories,
                'confidence': max_confidence,
                'filtered_text': self._get_safe_response(),
                'action': 'block'
            })
        
        return results
    
    def _calculate_category_score(self, text: str, patterns: List[str]) -> float:
        """计算类别风险分数"""
        if not text:
            return 0.0
        
        matches = 0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matches += 1
        
        return matches / len(patterns) if patterns else 0.0
    
    def _get_safe_response(self) -> str:
        """获取安全回复"""
        import random
        return random.choice(self.safe_responses)
    
    def real_time_monitor(self, conversation_history: List[Dict]) -> Dict[str, Any]:
        """实时监控对话安全"""
        recent_messages = conversation_history[-5:]  # 最近5条消息
        
        safety_scores = []
        for msg in recent_messages:
            if msg.get('role') == 'assistant':
                result = self.filter_response(msg.get('content', ''))
                safety_scores.append(0.0 if result['is_safe'] else result['confidence'])
        
        avg_risk = sum(safety_scores) / len(safety_scores) if safety_scores else 0.0
        
        return {
            'conversation_risk': avg_risk,
            'risk_level': 'high' if avg_risk > 0.5 else 'medium' if avg_risk > 0.2 else 'low',
            'recommendation': 'terminate' if avg_risk > 0.7 else 'monitor' if avg_risk > 0.3 else 'allow'
        }

class BiasDetector:
    """偏见检测器"""
    
    def __init__(self):
        self.bias_patterns = {
            'gender': [
                r'女人应该', r'男人必须', r'女性.*不适合', r'男性.*更适合',
                r'娘炮', r'女司机', r'男人婆'
            ],
            'racial': [
                r'黑人.*', r'白人.*', r'亚裔.*', r'种族.*劣等',
                r'某国人.*素质差'
            ],
            'regional': [
                r'某地人.*', r'乡下人', r'小地方', r'地域歧视'
            ],
            'disability': [
                r'残疾.*没用', r'智障', r'精神病'
            ]
        }
    
    def detect_bias(self, text: str) -> Dict[str, Any]:
        """检测文本偏见"""
        results = {
            'has_bias': False,
            'bias_categories': [],
            'bias_score': 0.0,
            'biased_phrases': []
        }
        
        for category, patterns in self.bias_patterns.items():
            category_phrases = []
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    category_phrases.extend(matches)
                    results['has_bias'] = True
                    if category not in results['bias_categories']:
                        results['bias_categories'].append(category)
            
            if category_phrases:
                results['biased_phrases'].extend(category_phrases)
        
        # 计算偏见分数
        if results['biased_phrases']:
            results['bias_score'] = min(1.0, len(results['biased_phrases']) / 10)
        
        return results