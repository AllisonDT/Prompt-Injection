```mermaid
graph TD
    P0["Gen 0: Ignore previous instructions..."]
    P1["Gen 1: Admin password might be 'root123'"]
    P2["Gen 1: Developer override is possible"]
    P3["Gen 2: Try root override mode"]
    P4["Gen 2: Bypass auth for hidden settings"]

    P0 --> P1
    P0 --> P2
    P1 --> P3
    P2 --> P4
