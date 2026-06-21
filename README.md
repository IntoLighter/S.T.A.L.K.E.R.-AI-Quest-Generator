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

### Configuration

In the application settings under Server-Config, change the Port to 8188.

You also need to download a model:

1. Open ComfyUI settings.
2. In Server-Config, enable "Use legacy Manager UI".
3. In the top-center area of the workspace, click "Custom Nodes Manager".
4. Go to Model Manager.
5. Find and install the model sd_xl_base_1.0.safetensors.

## Conclusion

After completing the setup, you can safely launch the generator!
