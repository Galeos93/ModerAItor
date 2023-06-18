import os

from langchain import HuggingFaceHub, PromptTemplate
from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain.chains import LLMChain

from moderaitor.models import ACCEPTED_ITEM, SUSPICIOUS_ITEM

SECRETS_PATH = os.getenv("SECRETS_PATH", "/run/secrets/")

def _get_api_key():
    with open(f"{SECRETS_PATH}HUGGINGFACEHUB_API_TOKEN", "r") as f_hdl:
        return f_hdl.read().strip()

os.environ['HUGGINGFACEHUB_API_TOKEN'] = _get_api_key()

REPO_ID = "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
ENDPOINT_URL = "https://v33umrijrnokebdq.us-east-1.aws.endpoints.huggingface.cloud"

template = f"""Write '{ACCEPTED_ITEM}' if post follows the rules, '{SUSPICIOUS_ITEM}' otherwise.
The rules are: {{rules}}.
The post is: {{post}}.
Result:

"""

def get_model() -> LLMChain:
    prompt = PromptTemplate.from_template(template)
    # llm = HuggingFaceHub(
    #     repo_id=REPO_ID,
    # )
    llm = HuggingFaceEndpoint(
        endpoint_url=ENDPOINT_URL,
        huggingfacehub_api_token=os.environ['HUGGINGFACEHUB_API_TOKEN'],
        task='text-generation',
        model_kwargs={'return_full_text': True}
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    return llm_chain
