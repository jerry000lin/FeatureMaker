def generate_customer_label(row: dict) -> dict:

    if row.get('credit_score') >=650 and row.get('risk_score') < 40:
        return {
            "llm_label": "可推荐",
            "llm_reason": "信用良好，风险较低"
        }
    elif row.get('risk_score') > 70:
        return {
            "llm_label": "不推荐",
            "llm_reason": "风险过高"
        }
    else:
        return {
            "llm_label": "谨慎推荐",
            "llm_reason": "需要进一步评估"
        }
