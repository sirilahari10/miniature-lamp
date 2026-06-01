import pandas as pd
import networkx as nx
import difflib


#INGESTION: SIMULATE MESSY MUNICIPAL DATA
def ingest_municipal_permits():
    print("[INFO] Ingesting messy municipal permit data...")
    raw_data = [
        {"permit_id": "AQ-2026-881", "applicant_name": "Grn Mtn Coffee LLC", "site": "Vermont", "permit_type": "Air Quality", "notes": "Installing new roasters. NOx limit 15ppm. Req: Catalytic Oxidizer."},
        {"permit_id": "BLD-2026-102", "applicant_name": "Tesla Inc.", "site": "Austin", "permit_type": "Expansion", "notes": "Stamping press foundation."},
        {"permit_id": "AQ-2026-904", "applicant_name": "Green Mountain Coffe Roasters", "site": "VT", "permit_type": "Emissions", "notes": "CO limit 50ppm."}
    ]
    return raw_data

#PROBABILISTIC ENTITY RESOLUTION
def resolve_entities(raw_data):
    print("[INFO] Running probabilistic Entity Resolution...")
    canonical_entities = ["Green Mountain Coffee", "Tesla", "Intel Corporation", "Ford Motor Company"]
    
    resolved_data = []
    for record in raw_data:
        matches = difflib.get_close_matches(record['applicant_name'], canonical_entities, n=1, cutoff=0.4)
        canonical_name = matches[0] if matches else "UNKNOWN_ENTITY"
        
        record['canonical_entity'] = canonical_name
        resolved_data.append(record)
        
    return resolved_data

# KNOWLEDGE GRAPH CONSTRUCTION
def build_knowledge_graph(resolved_data):
    print("[INFO] Constructing Industrial Knowledge Graph...")
    G = nx.DiGraph() # Directed Graph simulating Neo4j
    
    for record in resolved_data:
        entity = record['canonical_entity']
        permit = record['permit_id']
        
        G.add_node(entity, type="Company")
        G.add_node(permit, type="Permit", details=record['notes'])
        
        G.add_edge(entity, permit, relation="FILED_PERMIT")
        
        if "Catalytic Oxidizer" in record['notes']:
            G.add_node("Catalytic Oxidizer", type="Equipment")
            G.add_edge(permit, "Catalytic Oxidizer", relation="REQUIRES_EQUIPMENT")
            
        if "NOx" in record['notes'] or "CO" in record['notes']:
            G.add_node("Emissions Compliance", type="Requirement")
            G.add_edge(permit, "Emissions Compliance", relation="SUBJECT_TO")
            
    return G

#SIGNAL EXTRACTION (THE PRODUCT VALUE)
def extract_buying_signals(graph):
    print("-" * 50)
    for node, data in graph.nodes(data=True):
        if data.get('type') == 'Company' and node == "Green Mountain Coffee":
            print("[INDAX BUYING SIGNAL DETECTED]")
            print(f"Target: {node} (Vermont Facility)")
            
            permits = [v for u, v in graph.out_edges(node) if graph.edges[u, v]['relation'] == 'FILED_PERMIT']
            for permit in permits:
                print(f"Signal: Air Quality Permit ({permit}) filed for facility expansion.")
                
                equipment = [v for u, v in graph.out_edges(permit) if graph.edges[u, v]['relation'] == 'REQUIRES_EQUIPMENT']
                if equipment:
                    print(f"Equipment Needed: {', '.join(equipment)}, Industrial Roasters")
                    
            print("Permitted Limits: NOx=15ppm, CO=50ppm")
            print("Action: Route to Emissions Control OEM Sales Team.")
            print("-" * 50)
            
if __name__ == "__main__":
    raw_permits = ingest_municipal_permits()
    resolved_permits = resolve_entities(raw_permits)
    kg = build_knowledge_graph(resolved_permits)
    extract_buying_signals(kg)
