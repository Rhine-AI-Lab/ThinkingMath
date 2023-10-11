from xinference.client import Client

client = Client("http://localhost:25689")

model_uid = client.launch_model(
    model_name="llama-2-chat",
    model_size_in_billions=13,
    quantization="q4_1"
)

model = client.get_model(model_uid)

chat_history = []
prompt = "What is the largest animal?"
model.chat(
    prompt,
    chat_history,
    generate_config={"max_tokens": 1024}
)
