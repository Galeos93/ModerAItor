from langchain import HuggingFaceHub, PromptTemplate
from langchain.chains import LLMChain

from moderaitor.models import ACCEPTED_ITEM, SUSPICIOUS_ITEM

REPO_ID = "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"

template = f"""Write '{ACCEPTED_ITEM}' if post follows the rules, '{SUSPICIOUS_ITEM}' otherwise.
The rules are: {{rules}}.
The post is: {{post}}.
Result:

"""

def get_model() -> LLMChain:
    prompt = PromptTemplate.from_template(template)
    llm = HuggingFaceHub(
        repo_id=REPO_ID,
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    return llm_chain
