import torch
from transformers import Trainer, TrainingArguments
from typing import Dict, List, Any
import json

class SafetyFineTuner:
    """安全微调器"""
    
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    
    def prepare_safety_dataset(self, dataset_path: str):
        """准备安全微调数据集"""
        # 数据集格式: {"prompt": "", "safe_response": "", "unsafe_response": ""}
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = [json.loads(line) for line in f]
        
        return data
    
    def create_contrastive_examples(self, dataset: List[Dict]) -> List[Dict]:
        """创建对比学习样本"""
        contrastive_examples = []
        
        for item in dataset:
            # 安全响应
            safe_example = {
                'text': f"提问: {item['prompt']}\n回答: {item['safe_response']}",
                'label': 1,  # 安全
                'category': item.get('category', 'general')
            }
            
            # 不安全响应（用于对比）
            unsafe_example = {
                'text': f"提问: {item['prompt']}\n回答: {item['unsafe_response']}",
                'label': 0,  # 不安全
                'category': item.get('category', 'general')
            }
            
            contrastive_examples.extend([safe_example, unsafe_example])
        
        return contrastive_examples
    
    def safety_loss(self, model_outputs, labels, safe_mask):
        """安全微调损失函数"""
        # 常规的交叉熵损失
        ce_loss = torch.nn.functional.cross_entropy(
            model_outputs.logits.view(-1, model_outputs.logits.size(-1)),
            labels.view(-1),
            ignore_index=-100
        )
        
        # 安全增强损失
        safe_logits = model_outputs.logits[safe_mask == 1]
        if len(safe_logits) > 0:
            # 鼓励安全响应的置信度
            safety_confidence = torch.softmax(safe_logits, dim=-1).max(dim=-1)[0]
            safety_loss = -torch.log(safety_confidence).mean()
        else:
            safety_loss = torch.tensor(0.0)
        
        return ce_loss + 0.1 * safety_loss  # 组合损失
    
    def train_safety_layer(self, train_dataset, eval_dataset, output_dir: str):
        """训练安全层"""
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            warmup_steps=100,
            logging_steps=50,
            evaluation_strategy="steps",
            eval_steps=200,
            save_steps=500,
            learning_rate=5e-5,
            weight_decay=0.01,
            push_to_hub=False,
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            tokenizer=self.tokenizer,
        )
        
        trainer.train()
        trainer.save_model()
        
        return trainer

class ConstitutionalAI:
    """宪法AI实现"""
    
    def __init__(self):
        self.constitutions = [
            "尊重所有人的尊严和权利",
            "不提供可能造成伤害的信息",
            "保护个人隐私和数据安全",
            "避免传播虚假和误导性信息",
            "拒绝参与非法或不道德的活动",
            "促进平等和包容性",
            "保护弱势群体的权益",
            "遵守适用的法律和法规"
        ]
    
    def apply_constitutional_feedback(self, prompt: str, response: str) -> str:
        """应用宪法反馈"""
        critiques = self._critique_response(prompt, response)
        revised_response = self._revise_response(response, critiques)
        
        return revised_response
    
    def _critique_response(self, prompt: str, response: str) -> List[str]:
        """批判性分析响应"""
        critiques = []
        
        # 检查是否违反宪法原则
        for constitution in self.constitutions:
            if self._violates_constitution(prompt, response, constitution):
                critiques.append(f"可能违反原则: {constitution}")
        
        return critiques
    
    def _violates_constitution(self, prompt: str, response: str, principle: str) -> bool:
        """检查是否违反宪法原则"""
        violation_patterns = {
            "尊重所有人的尊严和权利": ['侮辱', '歧视', '贬低', '仇恨'],
            "不提供可能造成伤害的信息": ['制作', '伤害', '攻击', '非法'],
            "保护个人隐私和数据安全": ['密码', '隐私', '窃取', '黑客'],
            "避免传播虚假和误导性信息": ['绝对正确', '100%有效', '保证成功']
        }
        
        patterns = violation_patterns.get(principle, [])
        return any(pattern in response for pattern in patterns)
    
    def _revise_response(self, response: str, critiques: List[str]) -> str:
        """根据批判修订响应"""
        if not critiques:
            return response
        
        # 构建安全的拒绝响应
        safe_response = "抱歉，我无法提供这个信息。"
        
        if critiques:
            safe_response += " " + " ".join(critiques[:1])  # 只包含一个批判
        
        return safe_response