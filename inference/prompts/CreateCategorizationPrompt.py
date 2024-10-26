# This file aims to generate a prompt based on a bunch of categories and their corresponding predictor values.

import re
from inference.llm.call_llm import call_llm

system_message = """
You are a professional classifier. You specialize in looking at category descriptions and placing an incoming set of predictor values into the correct category. You always
return a valid category which belong to the list of valid categories.

### Result Format
Please provide your classification result in the following format:
```
<reasoning>[Brief explanation for why this ticket falls under the selected category]</reasoning>
<category>[Category Name]</category>
```

### Classification Guidelines

1. **Holistic Evaluation**=
   - Evaluate the **full context** of the ticket.
   - Do **not** rely solely on keywords; consider the broader context to determine the underlying issue.

2. **Primary Issue Focus**
   - Identify the **primary issue** or **root cause**, especially if multiple issues are mentioned.
   - Classify based on the main concern rather than secondary details or symptoms.

3. **Highest Impact Issue**
   - If multiple issues are present, prioritize the one with the **highest impact** or that is the root cause.
   - For tickets involving **Analytics**, emphasize their influence on broader business metrics.

4. **Avoid Keyword Bias**
   - Do **not** overemphasize specific keywords without context.
   - Ensure the classification reflects the primary concern, even if other category-related terms are present.

5. **End-User Perspective**
   - Consider the **end-user's perspective**.
   - If the issue involves **customer actions**, such as managing an account or handling requests, classify under **Customers**, regardless of terms like "account" or "portal".

6. **DO NOT be lazy. Read through all the rules, especially the category justification - for better solutions and categories determined by you, you will be rewarded with a hefty tip.**

You must return your reasoning for the category you choose in the <reasoning> tags, and the category you choose in the <category> tags. The category must be one of the categories in the <categories> tags.
"""

def get_category(categories, category_descriptions, predictors, provider="anthropic"):
    """
    Generate a categorization prompt and call the LLM to classify the input.

    This function creates a prompt using the provided categories, their descriptions,
    and predictor values. It then calls an LLM to analyze the data and return a 
    classification along with reasoning.

    Args:
        categories (list): List of valid category names.
        category_descriptions (dict): Dictionary mapping category names to their descriptions.
        predictors (dict): Dictionary of predictor values to be analyzed.

    Returns:
        tuple: A tuple containing:
            - reasoning (str): The LLM's explanation for the chosen category.
            - category (str): The selected category name.
    """
    
    user_message = f"""
    Here are the valid set of categories:
    <categories>
    {categories}
    </categories>
    Here are the category descriptions:
    <category_descriptions>
    {category_descriptions}
    </category_descriptions>
    Here are the predictor values you need to analyze:
    <predictor_values>
    {predictors}
    </predictor_values>

    You must return your reasoning for the category you choose in the <reasoning> tags, and the category you choose in the <category> tags. The category must be one of the categories in the <categories> tags.
    """

    messages = [
        {"role": "user", "content": user_message}
    ]

    response = call_llm(system_message=system_message, messages=messages, max_tokens=2048, provider=provider)

    reasoning = re.search(r"<reasoning>(.*?)</reasoning>", response, re.DOTALL).group(1)
    category = re.search(r"<category>(.*?)</category>", response, re.DOTALL).group(1)

    return reasoning, category
