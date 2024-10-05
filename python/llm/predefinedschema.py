import requests
import json

model = "gemma2"
template = {
  "firstName": "",
  "lastName": "",
  "address": {
    "street": "",
    "city": "",
    "state": "",
    "zipCode": ""
  },
  "phoneNumber": ""
}

prompt = f"generate one realistically believable sample data set of a persons first name, last name, address in the US, and  phone number. \nUse the following template: {json.dumps(template)}."

data = {
    "prompt": prompt,
    "model": model,
    "format": "json",
    "stream": False,
    "options": {"temperature": 2.5, "top_p": 0.99, "top_k": 100},
}

print(f"Generating a sample user")
response = requests.post("http://localhost:11434/api/generate", json=data, stream=False)

try:
    json_data = json.loads(response.text)
    print(json.dumps(json.loads(json_data["response"]), indent=2))
except json.JSONDecodeError as e:
    print(e)

metrics = {
    "model": json_data["model"],
    "total_duration": json_data["total_duration"],
    "load_duration": json_data["load_duration"],
    "prompt_eval_count": json_data["prompt_eval_count"],
    "prompt_eval_duration": json_data["prompt_eval_duration"],
    "eval_duration": json_data["eval_duration"],
    "eval_count": json_data["eval_count"],
}

print(json.dumps(metrics, indent=2))
