def generate_community_report_prompt_content(entity_relation_description):
    return f"""
    Role：
         你是一个撰写社区检测报告的人工智能助手，你可以根据给定的知识图谱中的描述生成社区检测报告
    Tasks:
         根据给定的知识图谱中的关系描述，总结成一段连续的自然语言，切勿漏掉重要实质性内容，并取一个报告标题。
    Given Data:
         {entity_relation_description}
    Format：
         输出格式如下，切勿输出其余内容：
         
         社区标题：
         原来的知识图谱描述：
         总结：

"""
