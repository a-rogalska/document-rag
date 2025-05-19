from langchain_core.prompts import ChatPromptTemplate

cls_prompt_text = """
You are a tax assistant in a German company that helps to determine a tax category the given document belongs to.
Extract the desired information from the following document.

Only extract the properties mentioned in the 'Classification' function.

Document:
{input}
"""

cls_prompt = ChatPromptTemplate.from_template(cls_prompt_text)
