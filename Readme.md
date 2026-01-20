# 🌾 Aksara Farming Advisor

Aksara Farming Advisor is an **AI-powered farming assistant** built using **Flask**, **llama-cpp-python**, and a modern streaming chat UI.  
It leverages the **Aksara v1 GGUF LLM** to provide **structured, agriculture-focused responses** for farmers and agriculture enthusiasts.
- Model URL: [huggingFace/cropinailab/aksara_v1](https://huggingface.co/cropinailab/aksara_v1)
- Github Repo: [github/Cropin-AILab/aksara](https://github.com/Cropin-AILab/aksara)

# Description by the CropinAILab
akṣara, is a Micro Language Model ((µ-LM)) and is a fine-tuned version of the Mistral-7B-Instruct-v0.2 model. The model is fine-tuned using proprietary and open-source agricultural data. The data is specific to five countries in the global south: India, Bangladesh, Sri Lanka, Pakistan and Nepal, and covers nine of the major crops of the region like paddy/rice, wheat, maize, barley, sorghum, cotton, sugarcane, millets, soybean. It was compressed by using the QLoRA technique that compresses the model from 16-bit to 4-bit precision leading to a 60% reduction in the model size! It gives about 40% more relevant ROUGE score than GPT-4 Turbo on randomly selected test datasets.

The knowledge domain of the model is specific to the agricultural best practices, including climate-smart agricultural practices (CSA) and regenerative agricultural practices (RA) for the above-mentioned focus countries and crops. More geographies and crops will be added later. The model is trained on a database containing information from seed sowing to harvesting, covering every phenological stage of the crop growth cycle and different aspects like crop health management, soil management, disease control, and others. The end-to-end pipeline incorporates various aspects of Responsible AI (RAI), like considering local features and preventing harmful content or misinformation.

The following hyperparameters were used during training:

learning_rate: 2e-4 train_batch_size: 4 eval_batch_size: 4 optimizer: paged_adam_32bit lr_scheduler_type: cosine num_epochs: 1 lora_r: 32 weight_decay: 0.001 For full details of this model please read our release blog post here. The technical details for the background, fine-tuning and reproducibility will be shared as a pre-print on arxiv very soon. The model can be inferenced on our Huggingface Space aksara spaces For framework versions, please refer to the requirements.txt file.

Developed by: Cropin AI Lab Contact: ailabs@cropin.com

Limitations The knowledge of akṣara is limited to the specific region and crops. We are looking forward to engage with the community on ways to make it better on the model, data, pipeline and "Responsible AI".

Disclaimer Beta Test version #1.0 - aksara is your agricultural AI advisor. Expect inaccuracies. We’re in active development stage to constantly learn & improve.

Blog: https://www.cropin.com/blogs/introducing-aksara-a-digital-agronomist First Version release: April 16, 2024.

Demo: https://huggingface.co/spaces/cropinailab/aksara Model Card: https://huggingface.co/cropinailab/aksara_v1

---

## 🚀 Features

- 🤖 **Local LLM (GGUF)** using `llama-cpp-python`
- 🌱 **Strict agriculture-only responses**
- 🧠 **Strong system prompt enforcement**
- 📡 **Real-time streaming responses**
- 🌐 **Modern chat UI (HTML, CSS, JavaScript)**
- 🔐 **CORS enabled API**
- 🌍 **Ngrok support for public access**
- 🇮🇳 **English & Hindi (Devanagari) support**
- ⚡ GPU acceleration support

---

## 🗂️ Project Structure

```
aksara-farming-advisor/
│
├── app.py
├── test_aksara_v1.ipynb
├── Aksara Farming AI Test Questions.docx
├── templates/
│   └── index.html
└── README.md
```

---

## 🧠 Model Details

- **Model:** `aksara_v1.Q4_K_M.gguf`
- **Format:** GGUF (4-bit quantized)
- **Source:** Hugging Face – `cropinailab/aksara_v1_GGUF`
- **Context Length:** 4096 tokens
- **GPU Support:** Enabled (`n_gpu_layers = -1`)

---

## ⚙️ Requirements

### Python
- Python **3.9+** recommended

### System
- NVIDIA GPU (optional but recommended)
- CUDA 12.x (for GPU acceleration)

---

## 📦 Installation

```bash
pip install flask flask-cors llama-cpp-python pyngrok huggingface_hub
```

For GPU support (CUDA 12.1):
```bash
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
```
---

## ▶️ Running the Application

```bash
python app.py
```

Once started, you will see:
- Local URL: `http://127.0.0.1:5000`
- Public Ngrok URL (printed in terminal)

---

## 🧪 API Endpoints

| Endpoint | Method | Description |
|--------|-------|-------------|
| `/` | GET | Web UI |
| `/chat` | POST | Non-streaming chat |
| `/chat_stream` | POST | Streaming chat |
| `/reset` | POST | Reset conversation |
| `/debug` | GET | Debug info |
| `/test_format` | GET | Test response format |

---

## 📌 Response Format

Every response strictly follows:

```
🌾 **Main Answer**

📋 **Key Points:**
• Point 1
• Point 2
• Point 3

💡 **Pro Tip:** Helpful farming advice
```

---
