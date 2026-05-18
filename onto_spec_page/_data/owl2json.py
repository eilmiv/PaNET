import requests
from functools import cache

from rdflib import Graph, URIRef, RDFS, SDO, paths

@cache
def query_pan_training(url):
    """Query the PaN-Training API for the given URL."""
    return requests.get(url, headers={"Accept": "application/json"}).json()

def enrich(graph, verbose=False):
    """Enricht the given rdf graph with additional information helpful for presentation."""
    # Add PaN-Training url if materials exist for the term
    techniques = set(graph.subjects(RDFS.subClassOf * paths.ZeroOrMore, URIRef("http://purl.org/pan-science/PaNET/PaNET00001")))
    
    if verbose:
        print("Querying PaN-Training for technique training")
    for i, term in enumerate(techniques):
        if verbose:
            print(f"  {i+1}/{len(techniques)}: {term}", end=" ", flush=True)
        training_url = f"https://pan-training.eu/ontology-term-search?iri={term}"
        try:
            if query_pan_training(training_url):
                graph.add((term, SDO.subjectOf, URIRef(training_url)))
                if verbose:
                    print("✓")
            elif verbose:
                print()
        except requests.RequestException as e:
            if verbose:
                print("✗")

    # add other related information here...

# Load the OWL file (RDF/XML format)
g = Graph()
g.parse("PaNET.owl", format="xml")  # Replace with your file path
enrich(g, verbose=True)

# Serialize to JSON-LD (standardized RDF-to-JSON format)
jsonld_data = g.serialize(format="json-ld")

# Save to a JSON file
with open("PaNET.json", "w") as f:
    f.write(jsonld_data)

print("Conversion of PaNET.owl complete! Output saved to PaNET.json")


# Load the OWL file (RDF/XML format)
g = Graph()
g.parse("PaNET_reasoned.owl", format="xml")  # Replace with your file path
enrich(g)

# Serialize to JSON-LD (standardized RDF-to-JSON format)
jsonld_data = g.serialize(format="json-ld")

# Save to a JSON file
with open("PaNET_reasoned.json", "w") as f:
    f.write(jsonld_data)

print("Conversion of PaNET_reasoned.owl complete! Output saved to PaNET_reasoned.json")



# Load the Turtle file
g = Graph()
g.parse("PaNET_metadata.ttl", format="turtle")

# Serialize to JSON-LD
jsonld_data = g.serialize(format="json-ld", indent=2)

# Save to a file
with open("PaNET_metadata.json", "w") as f:
    f.write(jsonld_data)

print("Conversion PaNET_metadata.ttl complete! Output saved to metadata.json")
