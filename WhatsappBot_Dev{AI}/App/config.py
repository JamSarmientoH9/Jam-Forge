import tkinter as tk
import openai

load_dotenv()
api_key = environ['OPENAI_API_KEY']

def spawn_models(roles: list[str], types: list[str], queries: list[str]):
    role_counter = 0
    for role in roles:
        ask model(types[role_counter], role, queries[role_counter])
        role_counter += 1
    ask_qa()
    ask_manager(
        "system",
        "All models answered! Time to decide@ \
        If you are ready to asnwer the user the don't run any functions and respond in a normal way. Otherwise, run the function again. \
        REMEMBER TO LISTEN TO THE QA!"
    )

# Define the function dictionary

rol_model = {
    "spawn_roles": spawn_models
}


#jhuomar aca va el request que tiene que tomar por condiciones el model, message_history, model fuctiones y que ten valor none ya tu te encargas de conectar esto
# pregunta al modelo de roles

def ask_model(type, role, query = None, history_override = None, is_user = False):
    if role != "": #define el parametro jhuomar
        print(f"asking model of role {role} and {'low' if type == 'dumb' else 'high'}...")
    else:
        print(f"asking QA...")
    
    own_history = []

    if len(own_history) == 0:
        if role != "Quality Assurance":
            own_history.append({ "role": "system", "content": model_initial_message.format(type = type, role = role) }) #definir inicializador
        else:
            own_history.append({ "role": "system", "content": qa_initial_message }) #definir el tester inicializador

    if history_override is not None:
        own_history = history_override + own_history
    if query is not None:
        own_history.append({ "role": "user" if is_user is True else "system", "content": query })

    response = send_request("gpt-3.5-turbo" if type == "dumb" else "gpt-4", own_history)
    response_message = response.choices[0].message

    history.append({ "role": "system", "content": f"model of role {role} and {'low' if type == 'dumb' else 'high'} IQ said: {response_message['content']}"})    
    
    if role == "Quality Assurance":
        print("-" * 50)
        print("QA Said:\n")
        print(response_message["content"])