![Text logo](docs/image/text_logo.jpg)

# First launch

## Text Generation

The application provides two text generation modes: local and remote.
Higher quality results are achieved when using larger models.
The generation type is selected in the application settings.

### Local Text Generation

#### Installing Ollama

Download and install: https://ollama.com

Check installation:
```
ollama --version
```

#### Downloading a Model

It is recommended to use top-performing models from leaderboards:

https://artificialanalysis.ai/leaderboards/models?weights=open<br>
https://llm-stats.com/leaderboards/open-llm-leaderboard

Example download:
```
ollama pull qwen3.6:35b
```

#### Running Ollama

Launch Ollama from the Start menu.

### Remote Text Generation

#### Installing LLM API Key Proxy

Download and extract:
https://github.com/Mirrowel/LLM-API-Key-Proxy/releases/tag/main%2Fbuild-20260123-1-bf7ab7e

#### Obtaining an API Key

Get an API key from any provider and enter it into the application.
More details here:
https://github.com/danclave/TALKER/blob/main/docs/Free_Models_Guide.md

## Icon Generation

Icons are generated locally using ComfyUI.

### Installing ComfyUI

Download and install: https://www.comfy.org/download

### Installing models

Download and install models to specified locations.

**diffusion_models**

- [flux-2-klein-9b-fp8.safetensors](https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-fp8/resolve/main/flux-2-klein-9b-fp8.safetensors)

**text_encoders**

- [qwen_3_8b_fp8mixed.safetensors](https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors)

**vae**

- [full_encoder_small_decoder.safetensors](https://huggingface.co/black-forest-labs/FLUX.2-small-decoder/resolve/main/full_encoder_small_decoder.safetensors)


#### Model Storage Location

```
📂 ComfyUI/
├── 📂 models/
│   ├── 📂 diffusion_models/
│   │   └── flux-2-klein-9b-fp8.safetensors
│   ├── 📂 text_encoders/
│   │   └── qwen_3_8b_fp8mixed.safetensors
│   └── 📂 vae/
│       └── full_encoder_small_decoder.safetensors
```

## Conclusion

After completing the setup, you can safely launch the generator!
