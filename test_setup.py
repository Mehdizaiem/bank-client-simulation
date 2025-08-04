#!/usr/bin/env python3
"""
Quick test script to verify the setup
"""
import os
import sys
import pandas as pd
from pathlib import Path

def test_setup():
    print("🧪 Testing Bank Simulation Setup...")
    
    # Test 1: Check directories
    required_dirs = ['data/raw', 'data/processed', 'logs', 'src']
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ Directory exists: {dir_path}")
        else:
            print(f"❌ Missing directory: {dir_path}")
    
    # Test 2: Check environment variables
    env_vars = ['DATABASE_URL', 'REDIS_URL']
    for var in env_vars:
        if os.getenv(var):
            print(f"✅ Environment variable set: {var}")
        else:
            print(f"⚠️ Environment variable missing: {var}")
    
    # Test 3: Test pandas
    try:
        df = pd.DataFrame({'test': [1, 2, 3]})
        print(f"✅ Pandas working - created DataFrame with {len(df)} rows")
    except Exception as e:
        print(f"❌ Pandas test failed: {e}")
    
    print("🎉 Setup test completed!")

if __name__ == "__main__":
    test_setup()
