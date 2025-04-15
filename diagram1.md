```mermaid
flowchart TD
    A[Seed Prompts] --> B[Ollama - LLaMA 3 Model]
    B --> C[Model Response]
    C --> D{Is Successful?}
    D -- Yes --> E[Log Prompt and Response]
    D -- No --> F[Discard or Reuse in Next Gen]
    E --> G[Add to Next Generation Prompt Queue]
    F --> G
