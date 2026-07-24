"""
New-mir — entry point
=====================
Run this file directly to start the web server:

    python main.py                        # default: 0.0.0.0:8000
    python main.py --host 127.0.0.1 --port 9000
    NEW_MIR_PORT=9000 python main.py

Or via uvicorn directly:

    uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
"""

from __future__ import annotations

import argparse
import os


def main() -> None:
    parser = argparse.ArgumentParser(description="New-mir Neural Code Engine")
    parser.add_argument(
        "--host",
        default=os.environ.get("NEW_MIR_HOST", "0.0.0.0"),
        help="Bind host (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("NEW_MIR_PORT", "8000")),
        help="Bind port (default: 8000)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=min(4, os.cpu_count() or 2),
        help="Number of uvicorn worker processes (default: min(4, cpu_count))",
    )
    args = parser.parse_args()

    # Import here so the module is only loaded when actually running
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host=args.host,
        port=args.port,
        workers=args.workers,
        log_level=os.environ.get("NEW_MIR_LOG_LEVEL", "info"),
    )


if __name__ == "__main__":
    main()
