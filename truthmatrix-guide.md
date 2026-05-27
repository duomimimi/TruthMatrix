# TruthMatrix 使用指南

> AI输出验证层——多层交叉检验，让幻觉无处遁形

---

## 核心概念

TruthMatrix 是一个**AI输出验证框架**，它的核心职责是：在AI生成的内容到达用户之前，进行多层次的事实核查和质量验证。

**为什么重要？**

当前所有大语言模型都会产生"幻觉"——看似合理但实际错误的内容。幻觉的来源包括：
- 训练数据中的错误信息
- 推理过程中的逻辑偏差
- 边界条件下的胡说八道
- 混合多源信息时的张冠李戴

TruthMatrix 通过三层验证机制解决这个问题：
1. **事实层**：验证输出中的客观事实是否准确
2. **逻辑层**：检查推理链条是否自洽
3. **一致性层**：确保输出与上下文、已知知识不矛盾

---

## 如何使用

### 第一步：初始化验证器

```python
from truthmatrix import Validator, FactChecker, LogicChecker

# 创建多层次验证器
validator = Validator(
    layers=[
        FactChecker(provider="serp"),      # 事实层：联网核查
        LogicChecker(provider="local"),    # 逻辑层：本地规则
        ConsistencyChecker()               # 一致性层：上下文比对
    ],
    threshold=0.85  # 置信度低于85%即标记为可疑
)
```

### 第二步：对AI输出进行验证

```python
async def process_with_verification(prompt: str, ai_output: str):
    # 使用NexusCore获取AI输出
    from nexuscore import Router
    router = Router(models)
    raw_output = await router.route(prompt)

    # 交由TruthMatrix验证
    result = await validator.verify(raw_output, context=prompt)

    if result.is_healthy:
        return result.output  # 通过验证，直接返回
    else:
        # 标记可疑区域
        return result.output_with_annotations
```

### 第三步：处理验证失败

```python
result = await validator.verify(output, context=prompt)

if not result.is_healthy:
    print(f"发现 {len(result.issues)} 个问题:")
    for issue in result.issues:
        print(f"  [{issue.type}] {issue.description}")
        print(f"  原文: {issue.text}")
        print(f"  建议: {issue.suggestion}")

    # 可以触发重生成
    if result.confidence < 0.5:
        await regenerate_with_feedback(prompt, result.issues)
```

---

## 代码示例

```python
import asyncio
from truthmatrix import Validator, VerificationReport

async def agent_loop(prompt: str):
    validator = Validator(threshold=0.8)

    for attempt in range(3):
        # 获取AI输出
        output = await get_ai_response(prompt)

        # 验证输出
        report = await validator.verify(output, context=prompt)

        if report.is_healthy:
            return output

        # 验证失败，用反馈信息重新生成
        prompt = f"{prompt}\n\n请避免以下错误：{report.summary}"

    return "无法生成可靠输出，请人工介入"
```

---

## 适用场景

### 场景1：新闻内容审核
媒体AI在发布新闻前自动通过TruthMatrix验证，将虚假信息拦截在发布前。对于财经、体育等事实性要求高的领域，可将错误率降低90%以上。

### 场景2：医疗AI辅助诊断
诊断建议生成后，TruthMatrix自动核查：药物相互作用是否准确？剂量是否符合指南？与患者病史是否冲突？保障患者安全。

### 场景3：法律文档生成
合同条款生成后，验证器自动检查：引用的法律条款是否仍然有效？数字金额是否一致？各方权利是否平衡？

### 场景4：客服机器人质量控制
每一次自动回复都经过TruthMatrix验证，确保不给用户错误信息。特别是涉及价格、政策、有效期等敏感信息时。

---

## 与其他模块的关系

| 模块 | 关系 | 说明 |
|:----:|:----:|:-----|
| NexusCore | 前置依赖 | NexusCore提供AI输出，TruthMatrix负责验证 |
| QualityForge | 评分来源 | TruthMatrix的验证结果成为QualityForge的质量评分 |
| SelfMend | 触发源 | TruthMatrix发现严重问题时触发SelfMend的修复流程 |
| AgentHive | 验证节点 | AgentHive中可以有专门的"验证Agent"使用TruthMatrix |

**架构定位**：TruthMatrix是质量保障层，串联NexusCore和其他所有输出型模块，确保最终内容的可靠性。

---

## 验证报告解读

```python
report = await validator.verify(output, context=prompt)

print(f"""
验证结果: {'✅ 通过' if report.is_healthy else '❌ 失败'}
置信度: {report.confidence:.1%}
问题数: {len(report.issues)}

层级详情:
  事实层: {'✅' if report.fact_score > 0.8 else '⚠️'} {report.fact_score:.1%}
  逻辑层: {'✅' if report.logic_score > 0.8 else '⚠️'} {report.logic_score:.1%}
  一致性: {'✅' if report.consistency_score > 0.8 else '⚠️'} {report.consistency_score:.1%}
""")
```

---

## 下一步

- 查看 [QualityForge 指南](./qualityforge-guide.md) — 如何基于TruthMatrix构建自我改进系统
- 查看 [SelfMend 指南](./selfmend-guide.md) — TruthMatrix如何触发自我修复
- 开始集成：pip install truthmatrix

---

*TruthMatrix — 让AI输出从"尽力而为"升级为"值得信赖"*