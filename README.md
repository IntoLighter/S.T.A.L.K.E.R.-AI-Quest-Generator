![Text logo](docs/image/text_logo.jpg)

A quest generator for S.T.A.L.K.E.R. that helps mod makers develop story mods by generating quest ideas and code artifacts.

# Getting Started

This guide walks you through the first-time setup of the generator. You need to configure **two independent parts**:

1. [Text generation](#1-text-generation): open-source models (Ollama) **or** proprietary models (API key)
2. [Icon generation](#2-icon-generation): local (ComfyUI)

## Contents

- [1. Text Generation](#1-text-generation)
  - [Option A: Open-source models (Ollama)](#option-a-open-source-models-ollama)
  - [Option B: Proprietary models (API key)](#option-b-proprietary-models-api-key)
- [2. Icon Generation](#2-icon-generation)
- [3. Done](#3-done)

---

## 1. Text Generation

The application supports two types of text generation: **open-source** models and **proprietary** models.
Larger models produce higher-quality results. The generation type is selected in the application settings.

| | Open-source (Ollama) | Proprietary (API) |
|---|---|---|
| Cost | Free | Free tiers available, see the [Free Models Guide](https://github.com/danclave/TALKER/blob/main/docs/Free_Models_Guide.md) |
| Privacy | Everything stays on your PC (local versions) | Requests are sent to the provider |
| Requirements | GPU / RAM depending on the model | Internet connection and an API key |

### Option A: Open-source models (Ollama)

**1. Install Ollama**

Download and install it from [ollama.com](https://ollama.com), then verify:

```bash
ollama --version
```

**2. Download a model**

**Recommended: the Gemma 4 series (`gemma4`).** Among recent open models, only this series has good knowledge of the S.T.A.L.K.E.R. lore.

| Model | Type | Notes |
|---|---|---|
| `gemma4:26b` | MoE | Runs well on a PC with **8 GB of VRAM**. Best choice for most users. |
| `gemma4:31b` | Dense | Most likely, only the **cloud** version can be run on consumer hardware. |

Local model:

```bash
ollama pull gemma4:26b
```

Cloud model (requires an Ollama account):

```bash
ollama signin
ollama pull gemma4:31b-cloud
```

**3. Run Ollama**

Launch Ollama from the Start menu. To check that it is running and the model is available:

```bash
ollama list
```

### Option B: Proprietary models (API key)

**1. Install LLM API Key Proxy**

Download the [release build](https://github.com/Mirrowel/LLM-API-Key-Proxy/releases/tag/main%2Fbuild-20260123-1-bf7ab7e) and extract it to any folder.

**2. Get an API key**

Get a key from any provider and enter it in the application settings.
See the [Free Models Guide](https://github.com/danclave/TALKER/blob/main/docs/Free_Models_Guide.md) for a list of free options.

---

## 2. Icon Generation

Icons are generated locally using [ComfyUI](https://www.comfy.org/download).

> **Tested hardware:** the diffusion model was tested on a GPU with **8 GB of VRAM**.

**1. Install ComfyUI**

Download and install it from [comfy.org/download](https://www.comfy.org/download).

**2. Download the models**

Put each file into the matching folder:

| Type | Folder | File |
|---|---|---|
| Diffusion model | `ComfyUI/models/diffusion_models/` | [flux-2-klein-9b-fp8.safetensors](https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-fp8/resolve/main/flux-2-klein-9b-fp8.safetensors) |
| Text encoder | `ComfyUI/models/text_encoders/` | [qwen_3_8b_fp8mixed.safetensors](https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors) |
| VAE | `ComfyUI/models/vae/` | [full_encoder_small_decoder.safetensors](https://huggingface.co/black-forest-labs/FLUX.2-small-decoder/resolve/main/full_encoder_small_decoder.safetensors) |

Expected structure:

```
📂 ComfyUI/
└── 📂 models/
    ├── 📂 diffusion_models/
    │   └── flux-2-klein-9b-fp8.safetensors
    ├── 📂 text_encoders/
    │   └── qwen_3_8b_fp8mixed.safetensors
    └── 📂 vae/
        └── full_encoder_small_decoder.safetensors
```

**3. Restart ComfyUI** so it picks up the new models.

---

## 3. Done

Setup is complete. Make sure that:

- [ ] The text model is configured in settings.
- [ ] The LLM engine is running.
- [ ] ComfyUI is running with all three models in place

Now you can launch the generator!
