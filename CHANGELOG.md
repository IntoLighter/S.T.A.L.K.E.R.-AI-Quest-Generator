## 1.2.0 (2026-06-24)

### Feat

- add forced metadata formatting
- change save directories
- increase icon prompt height
- improve infoportions record
- new icon metaprompt
- add output of original generated icon
- new modern diffusion model
- improve error windows behavior
- remove configuration of sampling parameters
- sort result files into folders
- change file names of code records to those used in gamedata
- change encoding of not coding records to utf-8
- add opportunity to choose system or custom value for text parameters in preferences
- specify retries count for openai client operations
- add dropdown for selecting a model

### Fix

- Ollama generation fail
- ensure prompt from configurator is transferred to main window
- remove incorrect margin in prompt editor
- prevent gemma generating markdown in metadata
- prevent artifact generation from stopping on single failure
- ensure remaining artifacts are saved when one fails
- ComfyUI workflow startup issue
- prevent coding records corruption
- prevent hang when generating with new local models

### Docs

- update ComfyUI models installation instruction in README
- add first launch hint in README
- add text logo in README
- translate README from Russian to English
- improve wording of text generation section in README
- revise Ollama model recommendations in README

## 1.1.0 (2026-03-21)

### Feat

- add support for modifying text model parameters used in concept generation
- add support for configuring image generation workflow
- add ability to open a prefilled GitHub issue form when an unknown error occurs
- increase default size of application windows

## 1.0.0 (2026-01-28)