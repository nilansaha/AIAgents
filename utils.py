import os
import pickle


def save_model(model, model_name):
    os.makedirs("saved_models", exist_ok=True)
    with open("saved_models/" + model_name + ".bin", "wb") as file:
        pickle.dump(model, file)


def load_model(model_name):
    model_location = "saved_models/" + model_name + ".bin"
    if not os.path.exists(model_location):
        return False

    with open(model_location, "rb") as file:
        model = pickle.load(file)
    return model
