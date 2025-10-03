# CKMT SDK

A Python SDK for the CKMT API

## Installation

```bash
pip install ckmt-python
```

Or install from source:

```bash
git clone https://github.com/projektckmt/ckmt-python.git
cd ckmt-python
pip install -e .
```

## Quick Start

```python
from ckmt import CKMT

# Initialize the client
client = CKMT(api_key="your_api_key_here")

# Get host information
host = client.host("8.8.8.8")
print(host)

# Search for hosts
results = client.search("nginx", page=1, size=10)
for match in results['matches']:
    print(match['ip'])

# Get statistics
stats = client.stats()
print(f"Total hosts: {stats['total_hosts']}")

# Count results
count = client.count(port="443")
print(f"Hosts with port 443: {count['count']}")

# Get facets
facets = client.facets("apache", facets="country,port,service")
print(facets)
```

## Async Support

```python
import asyncio
from ckmt import AsyncCKMT

async def main():
    client = AsyncCKMT(api_key="your_api_key_here")

    # Search asynchronously
    results = await client.search("nginx")
    print(results)

    # Get host info
    host = await client.host("8.8.8.8")
    print(host)

asyncio.run(main())
```

## Features

### Search API
- `search()` - Search for hosts using various filters
- `host()` - Get all data for a specific IP
- `count()` - Count hosts matching filters
- `facets()` - Get aggregated statistics
- `ports()` - Get list of ports
- `services()` - Get list of services
- `stats()` - Get overall platform statistics

## API Methods

### Search Methods

#### search(query, **kwargs)
Search for hosts using various filters.

**Parameters:**
- `query` (str, optional): Search query
- `port` (int, optional): Filter by port
- `service` (str, optional): Filter by service
- `product` (str, optional): Filter by product
- `version` (str, optional): Filter by version
- `country` (str, optional): Filter by country code
- `asn` (str, optional): Filter by ASN
- `os` (str, optional): Filter by OS
- `vuln` (str, optional): Filter by vulnerability/CVE
- `http_title` (str, optional): Filter by HTTP title
- `http_status` (int, optional): Filter by HTTP status
- `technology` (str, optional): Filter by technology
- `page` (int): Page number (default: 1)
- `size` (int): Results per page (default: 10)

#### host(ip)
Get all data for a specific IP address.

**Parameters:**
- `ip` (str): IP address to lookup

#### count(query=None, port=None, country=None)
Count hosts matching filters.

**Parameters:**
- `query` (str, optional): Search query
- `port` (str, optional): Port number
- `country` (str, optional): Country code

#### facets(query=None, facets="country,port,service,technology")
Get aggregated statistics.

**Parameters:**
- `query` (str, optional): Search query
- `facets` (str): Comma-separated facets to return

## Error Handling

```python
from ckmt import CKMT, CKMTError

client = CKMT(api_key="your_key")

try:
    results = client.search("test")
except CKMTError as e:
    print(f"API Error: {e}")
```

## Configuration

You can configure the SDK using environment variables:

```bash
export CKMT_API_KEY="your_api_key"
export CKMT_BASE_URL="https://api.ckmt.io"  # Optional, defaults to https://api.ckmt.io
```

Then initialize without parameters:

```python
from ckmt import CKMT

client = CKMT()  # Uses environment variables
```

## License

MIT License
