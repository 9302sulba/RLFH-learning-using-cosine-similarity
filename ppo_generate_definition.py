# -*- coding: utf-8 -*-
"""PPO_training_definition.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ct03bIPf1-F5t1ikSQsZX1Mm0lVGEJT_
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
import torch
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

# Load baseline DataFrame
df_baseline = pd.read_pickle("/bsuscratch/sulbhamalviya/NLP/NLP-Final-Project/results_with_similarity.pkl")

# Load fine-tuned model
tokenizer = AutoTokenizer.from_pretrained("/bsuscratch/sulbhamalviya/NLP/NLP-Final-Project/ppo_finetuned_smol_binary/")
model = AutoModelForCausalLM.from_pretrained("/bsuscratch/sulbhamalviya/NLP/NLP-Final-Project/ppo_finetuned_smol_binary/").eval()

# Load embedding model (same as baseline, e.g., MiniLM)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Generate definitions using fine-tuned model
generated_defs = []
for word in tqdm(df_baseline["word"]):
    input_text = f"Define {word}"
    inputs = tokenizer(input_text, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=30, pad_token_id=tokenizer.eos_token_id)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    generated_defs.append(generated_text)

# Add to DataFrame
df_baseline["definition_finetuned"] = generated_defs

# Compute cosine similarity with WordNet definitions
similarities_finetuned = []
for model_def, wordnet_def in zip(df_baseline["definition_finetuned"], df_baseline["wordnet_definition"]):
    emb1 = embedder.encode(model_def)
    emb2 = embedder.encode(wordnet_def)
    sim = cosine_similarity([emb1], [emb2])[0][0]
    similarities_finetuned.append(sim)

# Add new similarities
df_baseline["definition_similarity_finetuned"] = similarities_finetuned

# Keep only relevant columns
df_output = df_baseline[[
    "word",
    "definition_finetuned",
    "wordnet_definition",
    "definition_similarity_finetuned"
]]

# Save to pickle file
df_output.to_pickle("finetuned_definition_results.pkl")

# Shift in similarity
df_baseline["similarity_shift"] = df_baseline["definition_similarity_finetuned"] - df_baseline["definition_similarity"]

# Average improvement
improvement = df_baseline["similarity_shift"].mean()
print(f"Average similarity shift after PPO fine-tuning: {improvement:.4f}")
