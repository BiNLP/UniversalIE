from openai import AzureOpenAI
from pydantic import BaseModel

class Step(BaseModel):
    explanation: str
    output: str

class MathResponse(BaseModel):
    steps: list[Step]
    final_answer: str


REGION = "eastus"
MODEL = "gpt-4o-2024-08-06"
API_KEY = "02cbec6d675e4827c0c32c6965751cab"
API_BASE = "https://api.tonggpt.mybigai.ac.cn/proxy"
ENDPOINT = f"{API_BASE}/{REGION}"

client = AzureOpenAI( api_key=API_KEY, api_version="2024-08-01-preview", azure_endpoint=ENDPOINT, )

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor."},
        {"role": "user", "content": "solve 8x + 31 = 2"},
    ],
    response_format=MathResponse,
)

message = completion.choices[0].message
if message.parsed:
    print(message.parsed.steps)
    print(message.parsed.final_answer)
else:
    print(message.refusal)



# response = client.completions.create( model=MODEL, prompt="Once upon a time", )
# print(response.model_dump_json(indent=2))
# print(response.choices[0].text)

# response = client.chat.completions.create( model=MODEL, messages=[ {"role": "user", "content": "Say Hello!"} ], )
# print(response.model_dump_json(indent=2))
# print(response.choices[0].message.content)


