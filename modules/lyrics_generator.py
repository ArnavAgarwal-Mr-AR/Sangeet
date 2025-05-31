from transformers import pipeline

# Load model once
generator = pipeline("text-generation", model="gpt2")

def generate_line():
    prompt = "Spitting fire on the mic,"
    output = generator(prompt, max_length=20, do_sample=True, temperature=1.1)
    line = output[0]["generated_text"].replace(prompt, "").strip().split("\n")[0]
<<<<<<< HEAD
    return line
=======
    return line
>>>>>>> 957fad36ec8189a52f9eb4e6227089298cab2127
