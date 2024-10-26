# This file aims to generate a description of the target column based on the category-predictor dictionary.
# The inputs are going to be a bunch of categories and their corresponding predictor values.
# The output is going to be a description of the target column.

import re
from inference.llm.call_llm import call_llm

system_message = """
You are a professional analyzer of predictors. Your job is to, given a target value (encoded in <target>...</target> tags) and a set of predictor values (encoded in <predictor_values>...</predictor_values> tags), generate a description of what might cause the predictors to belong to the target class. The goal is to create a description that will help us grasp the underlying logic of the target column.

You must ensure the following:
1. The description is clear, concise, and to the point. It cannot mention specific values, but rather should be general enough to apply to all values that belong to the target class.
2. The description is not repetitive. It should not repeat the same thing for different predictor values.
3. You cannot be lazy - you will be rewarded for well-crafted descriptions and penalized for hyper-specific descriptions. Try to generate clear descriptions that will apply to most values that belong to the target class.
4. Return your thoughts in <reasoning>...</reasoning> tags, and the description in <description>...</description> tags.
5. Try to break your reasoning into small steps, and justify each step.
6. Using the small steps you have taken, generate a description that will help us understand the underlying logic of the target column.

Remember, you are being evaluated on the quality of your descriptions. You must follow the output format strictly - that is, return your thoughts in <reasoning>...</reasoning> tags, and the description in <description>...</description> tags.
"""

def get_target_description(category_name, category_predictor_dict):
    valid_predictor_values = category_predictor_dict[category_name]

    user_message = f"""
    <target>
    {category_name}
    </target>
    <predictor_values>
    {valid_predictor_values}
    </predictor_values>
    """

    messages = [
        {"role": "user", "content": user_message}
    ]

    response = call_llm(system_message=system_message, messages=messages, max_tokens=2048, provider="anthropic")

    reasoning = re.search(r"<reasoning>(.*?)</reasoning>", response, re.DOTALL).group(1)
    description = re.search(r"<description>(.*?)</description>", response, re.DOTALL).group(1)

    return reasoning, description