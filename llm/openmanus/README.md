# Open Manus for K8S

just a simple [Docker](https://www.docker.com/) image for [OpenManus](https://github.com/mannaandpoem/OpenManus)

If you want to play with OpenManus in a safe environment, you may run it in a Docker container using the Dockerfile from this repository.

## Instructions

### Build Image

```bash
docker buildx build . --tag openmanus:latest
```

Now, open file `./config/config.toml` with your favourite editor and enter your configuration details. If you plan to use [Ollama](https://ollama.com/) with a locally installed LLM (e.g., `qwen2.5-coder:14b`), the first lines of your configuration may look as follows:

```ini
# Global LLM configuration
[llm]
model = "qwen2.5-coder:14b"
base_url = "http://host.docker.internal:11434/v1"
api_key = "ollama"
max_tokens = 4096
temperature = 0.0
```

Save your changes, then open your terminal, navigate to your OpenManus folder and run the following command:

```bash
docker compose up
```

Docker will now download all required files (which may take a while, when run for the first time) and finally start the freshly built image.

Since OpenManus requires some input from the command line, you should now switch to the "Docker Desktop", select the OpenManus container (named "openmanus-1") and navigate to the "TTY". Here, you may now enter your prompt and watch OpenManus working.

## License

[MIT License](LICENSE.md)
