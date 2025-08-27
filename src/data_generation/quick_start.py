#!/usr/bin/env python3
"""
Quick Start Data Pipeline
Your first pipeline execution script
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent))

print("�� Quick Start - Bank Simulation Data Pipeline")
print("=" * 50)

# Test 1: Create sample data
print("📊 Creating sample data...")

# Simple retail client data
retail_data = {
    'client_id': [f'R_{i:05d}' for i in range(1, 101)],
    'age': np.random.randint(18, 80, 100),
    'income': np.random.uniform(500, 8000, 100),
    'governorate': np.random.choice(['Tunis', 'Sfax', 'Sousse', 'Ariana'], 100),
    'satisfaction': np.random.uniform(0.3, 1.0, 100)
}

retail_df = pd.DataFrame(retail_data)

# Save to processed folder
processed_dir = Path("../data/processed")
processed_dir.mkdir(exist_ok=True)

retail_df.to_csv(processed_dir / "quick_start_retail.csv", index=False)

print(f"✅ Created {len(retail_df)} retail client records")
print(f"   Saved to: data/processed/quick_start_retail.csv")

# Test 2: Basic statistics
print(f"\n📈 Quick Statistics:")
print(f"   Age range: {retail_df['age'].min()}-{retail_df['age'].max()}")
print(f"   Income range: {retail_df['income'].min():.0f}-{retail_df['income'].max():.0f} TND")
print(f"   Average satisfaction: {retail_df['satisfaction'].mean():.2f}")

print(f"\n🎉 Quick start completed successfully!")
print(f"   Next: Start working on your CTGAN pipeline")
print(f"   Your team can now use: data/processed/quick_start_retail.csv")
