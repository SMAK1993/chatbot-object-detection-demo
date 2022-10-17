from Chatbot import Chatbot


def chatbox_over_http(text):
    import requests
    MODEL_ENDPOINT = "http://10.152.183.11:8000"
    body = {
        "data": {
            "ndarray": text
        }
    }
    return requests.post(MODEL_ENDPOINT + "/api/v0.1/predictions", json=body)


# Local model execution
# model = Chatbot()

for step in range(10):
    user_input = input(f">> User {step}:")

    # res = model.predict(np.array(user_input), [])
    # print(res)

    res = chatbox_over_http(user_input)
    print(res.status_code, res.text)
