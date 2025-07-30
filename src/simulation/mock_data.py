# src/simulation/mock_data.py
import pandas as pd

def generate_mock_agents(n=1000):
    """Generate mock agent data with initial states."""
    data = pd.DataFrame({
        'unique_id': range(n),
        'demographics': [f"Tunis_{'Male' if i % 2 == 0 else 'Female'}" for i in range(n)],
        'channel_preference': ['mobile', 'branch', 'web'] * (n // 3) + ['mobile'] * (n % 3),
        'satisfaction_level': [0.5 for _ in range(n)],
        'status': ['active' for _ in range(n)]
    })
    return data

if __name__ == "__main__":
    mock_data = generate_mock_agents()
    mock_data.to_csv("mock_agents.csv", index=False)
    print(f"Mock data with {len(mock_data)} agents saved to mock_agents.csv")