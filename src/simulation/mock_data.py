import pandas as pd
import random
import os

def generate_mock_agents(n=50000):
    """Generate mock agent data with initial states."""
    data = pd.DataFrame({
        'unique_id': range(n),
        'demographics': [f"{random.choice(['Tunis', 'Sfax', 'Sousse', 'Djerba'])}_{'Male' if i % 2 == 0 else 'Female'}" for i in range(n)],
        'channel_preference': [random.choice(['mobile', 'branch', 'web']) for _ in range(n)],
        'satisfaction_level': [random.uniform(0.3, 0.7) for _ in range(n)],
        'status': ['active' for _ in range(n)],
        'income_level': [random.choice(['low', 'medium', 'high']) for _ in range(n)],
        'transaction_frequency': [random.randint(1, 10) for _ in range(n)],
        'region': [random.choice(['Tunis', 'Sfax', 'Sousse', 'Djerba']) for _ in range(n)]
    })
    return data

if __name__ == "__main__":
    root_path = r"C:\Users\asus\Documents\4DS1\Summer Internship\bank-client-simulation-project\bank-client-simulation"
    mock_data = generate_mock_agents()
    mock_data.to_csv(os.path.join(root_path, 'mock_agents_large.csv'), index=False)
    print(f"Mock data with {len(mock_data)} agents saved to {os.path.join(root_path, 'mock_agents_large.csv')}")