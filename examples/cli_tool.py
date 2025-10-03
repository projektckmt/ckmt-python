#!/usr/bin/env python3
"""
Simple CLI tool for CKMT API using the SDK
"""

import sys
import json
import argparse
from ckmt import CKMT, CKMTError

def format_json(data):
    """Pretty print JSON data."""
    return json.dumps(data, indent=2)

def main():
    parser = argparse.ArgumentParser(description="CKMT CLI - Query security data")
    parser.add_argument("--api-key", help="API key (or set CKMT_API_KEY env var)")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for hosts")
    search_parser.add_argument("query", nargs="?", help="Search query")
    search_parser.add_argument("--port", type=int, help="Filter by port")
    search_parser.add_argument("--service", help="Filter by service")
    search_parser.add_argument("--country", help="Filter by country code")
    search_parser.add_argument("--page", type=int, default=1, help="Page number")
    search_parser.add_argument("--size", type=int, default=10, help="Results per page")

    # Host command
    host_parser = subparsers.add_parser("host", help="Get host information")
    host_parser.add_argument("ip", help="IP address to lookup")

    # Count command
    count_parser = subparsers.add_parser("count", help="Count matching hosts")
    count_parser.add_argument("--query", help="Search query")
    count_parser.add_argument("--port", help="Filter by port")
    count_parser.add_argument("--country", help="Filter by country")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get platform statistics")

    # Facets command
    facets_parser = subparsers.add_parser("facets", help="Get aggregated facets")
    facets_parser.add_argument("--query", help="Search query")
    facets_parser.add_argument("--facets", default="country,port,service",
                               help="Comma-separated facets")

    # Ports command
    ports_parser = subparsers.add_parser("ports", help="Get list of ports")
    ports_parser.add_argument("--query", help="Search query")
    ports_parser.add_argument("--size", type=int, default=100, help="Number of results")

    # Services command
    services_parser = subparsers.add_parser("services", help="Get list of services")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        # Initialize client
        client = CKMT(api_key=args.api_key)

        # Execute command
        if args.command == "search":
            result = client.search(
                query=args.query,
                port=args.port,
                service=args.service,
                country=args.country,
                page=args.page,
                size=args.size
            )

        elif args.command == "host":
            result = client.host(args.ip)

        elif args.command == "count":
            result = client.count(
                query=args.query,
                port=args.port,
                country=args.country
            )

        elif args.command == "stats":
            result = client.stats()

        elif args.command == "facets":
            result = client.facets(
                query=args.query,
                facets=args.facets
            )

        elif args.command == "ports":
            result = client.ports(
                query=args.query,
                size=args.size
            )

        elif args.command == "services":
            result = client.services()

        else:
            parser.print_help()
            sys.exit(1)

        # Print result
        print(format_json(result))

    except CKMTError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
