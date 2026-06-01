# Indax: Real-Time Industrial Knowledge Graph (PoW)

the core of Indax is a real-time knowledge graph fed by continuous, large-scale data ingestion across municipal websites, ultimately turning fragmented data into OEM buying signals.

This repository demonstrates the foundational architecture required for this:
1. Messy Data Ingestion: Simulates scraping unstructured, inconsistent municipal air quality permits.
2. Probabilistic Entity Resolution: Reconciles inconsistent corporate names (e.g., "Grn Mtn Coffee LLC") to a canonical entity ("Green Mountain Coffee") using fuzzy string matching.
3. Knowledge Graph Construction:Builds a property graph linking the Facility, the Permit, the Equipment (Catalytic Oxidizers), and the permitted limits (NOx, CO).
4. Buying Signal Extraction: Traverses the graph to flag a high-value OEM sales opportunity before an RFQ is ever filed.
