"""Basic usage examples for CKMT SDK"""

from ckmt import CKMT

# Initialize client
client = CKMT(api_key="your_api_key_here")

# Example 1: Search for nginx servers
print("Searching for nginx servers...")
results = client.search("nginx", page=1, size=5)
print(f"Found {results['total']} results")
for match in results['matches']:
    print(f"  - {match['ip']}")

# Example 2: Get specific host information
print("\nGetting host information for 60.204.186.228...")
try:
    host = client.host("60.204.186.228")
    print(f"Host: {host['ip']}")
    print(f"Total records: {host['total']}")
except Exception as e:
    print(f"Error: {e}")

# Example 3: Search with multiple filters
print("\nSearching for Apache servers on port 443 in US...")
results = client.search(
    product="apache",
    port=443,
    country="US",
    size=10
)
print(f"Found {results['total']} matching hosts")

# Example 4: Get statistics
print("\nGetting platform statistics...")
stats = client.stats()
print(f"Total hosts: {stats['total_hosts']}")
print(f"Total ports: {stats['total_ports']}")
print(f"Total vulnerabilities: {stats['total_vulnerabilities']}")

# Example 5: Count results
print("\nCounting hosts with port 443 open...")
count = client.count(port="443")
print(f"Hosts with port 443: {count['count']}")

# Example 6: Get facets
print("\nGetting facets for 'apache'...")
facets = client.facets("apache", facets="country,port,service")
print(f"Total: {facets['total']}")
if 'countries' in facets:
    print("Top countries:")
    for country in facets['countries'][:5]:
        print(f"  - {country['value']}: {country['count']}")

# Example 7: Get list of ports
print("\nGetting list of ports...")
ports = client.ports(size=20)
print(f"Top ports: {ports['data'][:10]}")

# Example 8: Get list of services
print("\nGetting list of services...")
services = client.services()
print(f"Services: {services['services'][:10]}")
