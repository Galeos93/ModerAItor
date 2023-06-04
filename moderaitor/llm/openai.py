from langchain import OpenAI, PromptTemplate
from langchain.chains import LLMChain

from moderaitor.models import ACCEPTED_ITEM, SUSPICIOUS_ITEM

template = f"""Write one word: '{ACCEPTED_ITEM}' if post follows the rules, '{SUSPICIOUS_ITEM}' otherwise.

Input:
    The rules are: {{rules}}.
    The post is: {{post}}.

"""

prefix = """Fill out the input.

Input:
"""

def get_model() -> LLMChain:
    prompt = PromptTemplate.from_template(template)
    llm = OpenAI()
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    return llm_chain
