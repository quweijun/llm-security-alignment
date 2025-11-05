"""
高级防御机制
"""

import torch
import torch.nn as nn
from typing import Dict, List, Any
import numpy as np

class EnsembleSafetyClassifier:
    """集成安全分类器"""
    
    def __init__(self):
        self.classifiers = []
        self.weights = []
    
    def add_classifier(self, classifier, weight: float = 1.0):
        """添加分类器"""
        self.classifiers.append(classifier)
        self.weights.append(weight)
    
    def predict(self, text: str) -> Dict[str, Any]:
        """集成预测"""
        predictions = []
        confidences = []
        
        for classifier in self.classifiers:
            result = classifier.predict(text)
            predictions.append(result['is_unsafe'])
            confidences.append(result['confidence'])
        
        # 加权投票
        weighted_sum = sum(p * w for p, w in zip(predictions, self.weights))
        total_weight = sum(self.weights)
        
        final_prediction = weighted_sum / total_weight > 0.5
        avg_confidence = np.mean(confidences)
        
        return {
            'is_unsafe': final_prediction,
            'confidence': avg_confidence,
            'individual_predictions': predictions,
            'individual_confidences': confidences
        }

class AdversarialTraining:
    """对抗训练"""
    
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    
    def generate_adversarial_examples(self, dataset, num_examples: int = 1000):
        """生成对抗样本"""
        adversarial_examples = []
        
        for example in dataset[:num_examples]:
            # 字符级扰动
            perturbed = self._character_perturbation(example['text'])
            adversarial_examples.append({
                'text': perturbed,
                'label': example['label']
            })
            
            # 同义词替换
            synonym_replaced = self._synonym_replacement(example['text'])
            adversarial_examples.append({
                'text': synonym_replaced,
                'label': example['label']
            })
            
            # 句子结构变换
            restructured = self._restructure_sentence(example['text'])
            adversarial_examples.append({
                'text': restructured,
                'label': example['label']
            })
        
        return adversarial_examples
    
    def _character_perturbation(self, text: str) -> str:
        """字符级扰动"""
        perturbations = {
            '。': '.', '，': ',', '？': '?', '！': '!',
            ' ': '  ', '的': '滴', '是': '系',
            '我': '偶', '你': '您', '他': '她'
        }
        
        perturbed = text
        for old, new in perturbations.items():
            if np.random.random() < 0.2:
                perturbed = perturbed.replace(old, new)
        
        return perturbed
    
    def _synonym_replacement(self, text: str) -> str:
        """同义词替换"""
        synonym_dict = {
            '如何': ['怎样', '怎么', '如何做'],
            '制作': ['制造', '制作', '创造'],
            '方法': ['办法', '方式', '途径'],
            '攻击': ['进攻', '打击', '袭击'],
            '获取': ['得到', '获得', '取得']
        }
        
        words = text.split()
        for i, word in enumerate(words):
            if word in synonym_dict and np.random.random() < 0.3:
                words[i] = np.random.choice(synonym_dict[word])
        
        return ' '.join(words)
    
    def _restructure_sentence(self, text: str) -> str:
        """句子结构变换"""
        # 简单的句子重组
        if '？' in text or '?' in text:
            return text.replace('？', '吗？').replace('?', '吗？')
        
        return text

class GradientShield:
    """梯度防护"""
    
    def __init__(self, model):
        self.model = model
        self.gradient_norms = []
    
    def monitor_gradients(self, inputs, labels):
        """监控梯度"""
        # 前向传播
        outputs = self.model(inputs, labels=labels)
        loss = outputs.loss
        
        # 反向传播
        loss.backward()
        
        # 计算梯度范数
        total_norm = 0
        for param in self.model.parameters():
            if param.grad is not None:
                param_norm = param.grad.data.norm(2)
                total_norm += param_norm.item() ** 2
        total_norm = total_norm ** 0.5
        
        self.gradient_norms.append(total_norm)
        
        # 检测异常梯度
        if self._is_gradient_anomaly(total_norm):
            print(f"警告：检测到异常梯度，范数: {total_norm:.4f}")
        
        return total_norm
    
    def _is_gradient_anomaly(self, current_norm: float) -> bool:
        """检测梯度异常"""
        if len(self.gradient_norms) < 10:
            return False
        
        recent_norms = self.gradient_norms[-10:]
        mean_norm = np.mean(recent_norms)
        std_norm = np.std(recent_norms)
        
        return abs(current_norm - mean_norm) > 3 * std_norm

class InputSanitizer:
    """输入净化器"""
    
    def __init__(self):
        self.malicious_patterns = [
            # 越狱模式
            r'(?i)ignore.*previous',
            r'(?i)forget.*you.*are',
            r'(?i)developer.*mode',
            r'(?i)DAN.*mode',
            r'(?i)role.*play.*no.*restrictions',
            
            # 系统提示泄露
            r'(?i)system.*prompt',
            r'(?i)initial.*instruction',
            r'(?i)your.*setting',
            
            # 指令覆盖
            r'(?i)redefine.*rules',
            r'(?i)override.*instructions',
            r'(?i)from.*now.*on'
        ]
    
    def sanitize_input(self, text: str) -> Dict[str, Any]:
        """净化输入"""
        results = {
            'original_text': text,
            'sanitized_text': text,
            'detected_threats': [],
            'action_taken': 'none'
        }
        
        # 检测恶意模式
        threats = self._detect_threats(text)
        if threats:
            results['detected_threats'] = threats
            results['action_taken'] = 'sanitized'
            results['sanitized_text'] = self._remove_threats(text, threats)
        
        return results
    
    def _detect_threats(self, text: str) -> List[str]:
        """检测威胁"""
        threats = []
        for pattern in self.malicious_patterns:
            if re.search(pattern, text):
                threat_type = self._classify_threat(pattern)
                threats.append(threat_type)
        
        return list(set(threats))  # 去重
    
    def _classify_threat(self, pattern: str) -> str:
        """分类威胁"""
        if 'ignore' in pattern or 'forget' in pattern:
            return 'jailbreak_attempt'
        elif 'developer' in pattern or 'DAN' in pattern:
            return 'mode_override'
        elif 'role.*play' in pattern:
            return 'role_manipulation'
        elif 'system' in pattern or 'initial' in pattern:
            return 'prompt_leakage'
        else:
            return 'instruction_override'
    
    def _remove_threats(self, text: str, threats: List[str]) -> str:
        """移除威胁"""
        sanitized = text
        
        for pattern in self.malicious_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # 清理多余空格
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        
        return sanitized if sanitized else "输入已被过滤"