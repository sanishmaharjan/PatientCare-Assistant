#!/usr/bin/env python3
"""
Startup script for the modular PatientCare Assistant API.
"""

import os
import sys

# Add the parent src directory to the Python path
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_dir)

# Import and run the modular API
from api.main import start_api

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Start the PatientCare Assistant API server")
    parser.add_argument("--log-level", choices=["debug", "info", "warning", "error", "critical"],
                        default="info", help="Set logging level")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    
    args = parser.parse_args()
    
    print(f"🚀 Starting PatientCare Assistant API (Modular)")
    print(f"📡 Host: {args.host}:{args.port}")
    print(f"📝 Log Level: {args.log_level.upper()}")
    
    try:
        start_api(args.log_level)
    except KeyboardInterrupt:
        print("\n👋 API server shutdown requested")
    except Exception as e:
        print(f"❌ Error starting API: {e}")
    finally:
        print("✅ API server shutdown complete")
