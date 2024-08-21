import ollama

response = ollama.chat(
    model='llama3.1',
    messages=[{'role': 'user', 'content': 'Resume esto en csv: \
    https://viajes.nationalgeographic.com.es/a/ruta-literaria-por-paris_12147'}],
    stream=False,
)

print(response['message']['content'])
