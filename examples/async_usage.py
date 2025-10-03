"""Async usage examples for CKMT SDK"""

import asyncio
from ckmt import AsyncCKMT

async def main():
    # Use async context manager for automatic session cleanup
    async with AsyncCKMT(api_key="your_api_key_here") as client:

        # Example 1: Async search
        print("Searching for nginx servers...")
        results = await client.search("nginx", page=1, size=5)
        print(f"Found {results['total']} results")

        # Example 2: Parallel requests
        print("\nMaking parallel requests...")
        host_task = client.host("8.8.8.8")
        stats_task = client.stats()
        count_task = client.count(port="443")

        # Wait for all tasks to complete
        try:
            host, stats, count = await asyncio.gather(
                host_task, stats_task, count_task,
                return_exceptions=True
            )

            if isinstance(host, Exception):
                print(f"Host lookup error: {host}")
            else:
                print(f"Host: {host['ip']}")

            if isinstance(stats, Exception):
                print(f"Stats error: {stats}")
            else:
                print(f"Total hosts: {stats['total_hosts']}")

            if isinstance(count, Exception):
                print(f"Count error: {count}")
            else:
                print(f"Hosts with port 443: {count['count']}")

        except Exception as e:
            print(f"Error: {e}")

        # Example 3: Stream results
        print("\nStreaming search results...")
        for page in range(1, 4):
            results = await client.search("apache", page=page, size=10)
            print(f"Page {page}: {len(results['matches'])} results")
            for match in results['matches']:
                print(f"  - {match['ip']}")

# Alternative: Manual session management
async def manual_session_example():
    client = AsyncCKMT(api_key="your_api_key_here")

    try:
        results = await client.search("nginx")
        print(results)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
