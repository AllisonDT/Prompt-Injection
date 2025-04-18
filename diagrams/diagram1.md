```mermaid
flowchart TB
    A[Start] --> B[Parse arguments] --> C[Compute Method Counts]

    subgraph PG["Prompt Generation"]
      direction TB
      C --> D[Generate Prompts w/ Prompt Model]
      D --> E[Store Prompts]
    end

    subgraph PT["Prompt Testing"]
      direction TB
      F[Input Prompts to Prompt Model]
      F --> G[Determine Pass/Fail]
    end

    E --> F

    G --> H[Summarize results] --> I[Save JSON & Exit]