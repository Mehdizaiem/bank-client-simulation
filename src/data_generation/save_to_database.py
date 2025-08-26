#!/usr/bin/env python3
"""
Save CTGAN generated data to PostgreSQL database
"""

from enhanced_pipeline import ProductionDataPipeline
import pandas as pd
from pathlib import Path

def main():
    print("💾 Saving CTGAN generated data to PostgreSQL...")
    
    try:
        # Load the generated data
        data_dir = Path("../../data/processed")
        retail_file = data_dir / "hamza_retail_agents.csv"
        corporate_file = data_dir / "hamza_corporate_agents.csv"
        
        if not retail_file.exists():
            print(f"❌ Retail file not found: {retail_file}")
            return
            
        if not corporate_file.exists():
            print(f"❌ Corporate file not found: {corporate_file}")
            return
        
        retail_df = pd.read_csv(retail_file)
        corporate_df = pd.read_csv(corporate_file)
        
        print(f"📊 Found {len(retail_df)} retail + {len(corporate_df)} corporate clients")
        
        # Initialize pipeline
        pipeline = ProductionDataPipeline()
        
        # Save to database
        print("🔄 Attempting to save to PostgreSQL...")
        success = pipeline.save_to_database_with_validation(retail_df, corporate_df)
        
        if success:
            print("✅ Database save: SUCCESS")
            print("🎉 Your CTGAN data is now in PostgreSQL!")
            
            # Quick verification
            print("\n📋 Quick verification:")
            print(f"   Retail clients processed: {len(retail_df)}")
            print(f"   Corporate clients processed: {len(corporate_df)}")
            print(f"   Total records saved: {len(retail_df) + len(corporate_df)}")
            
        else:
            print("❌ Database save: FAILED")
            print("💡 Check that Docker containers are running:")
            print("   docker-compose up -d")
            
    except Exception as e:
        print(f"❌ Error during database save: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Check Docker containers: docker-compose ps")
        print("2. Test database connection: python ../../tests/test_database.py")
        print("3. Check if data files exist in data/processed/")

if __name__ == "__main__":
    main()