import yaml

with open('streamlit/data.yaml', 'r') as f:
    data = yaml.safe_load(f)

print(data)
