# Open Manus for K8S

just a simple [Docker](https://www.docker.com/) image for [OpenManus](https://github.com/mannaandpoem/OpenManus)

If you want to play with OpenManus in a safe environment, you may run it in a Docker container using the Dockerfile from this repository.

## Instructions

### Building the Docker Image

```bash
docker buildx build . --tag openmanus:latest
```

Open file `./config/config.toml` and enter your configuration details. If you plan to use [Ollama](https://ollama.com/) with a locally installed LLM (e.g., `qwen2.5-coder:14b`), the first lines of your configuration may look as follows:

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
docker run ...
```

## License

[MIT License](LICENSE.md)
