# RLFH-learning-using-cosine-similarity
baseline_model_NLP_Final_project.ipynb	This notebook establishes the baseline model. It loads a pretrained language model (e.g., SmolLM-135M) and generates definitions for a set of word prompts. The outputs are embedded and compared to WordNet definitions using cosine similarity. This serves as the baseline for later reward-based comparison. this file also has results of first experiemt when finetuned model with binary reward.

PPO_Training (1).ipynb
Implements PPO fine-tuning with two types of reward models:
• Binary reward: 1 if cosine similarity ≥ threshold (e.g., 0.85), else 0
• Soft reward: Direct cosine similarity value used as reward.
The model is updated using these signals to improve semantic alignment of generated definitions.

ppo_generate_definition.py: After model training and fine tuning with RLFH, generated definitions from the fine-tuned PPO model with soft reward model and binary reward model . Useful for evaluation or quick testing in batch mode.

PPO_finetuned_results.ipynb	Evaluates the fine-tuned models by comparing them with baseline outputs. Calculates cosine similarity gain, and percentage of improved definitions for both binary and soft reward models.
