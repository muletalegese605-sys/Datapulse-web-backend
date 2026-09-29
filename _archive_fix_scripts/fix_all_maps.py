import re
with open('public/index.html', 'r') as f:
    content = f.read()

# Variables hafan kanneen sirreessuuf
content = content.replace('state.records.map(', '(state.records || []).map(')
content = content.replace('datasets.map(', '(datasets || []).map(')
content = content.replace('prices.map(', '(prices || []).map(')
content = content.replace('state.audits.slice(0,100).map(', '(state.audits || []).slice(0,100).map(')
content = content.replace('state.audits.slice(0, 100).map(', '(state.audits || []).slice(0, 100).map(')

with open('public/index.html', 'w') as f:
    f.write(content)
print("Rakkoole hafan hundi sirreeffamaniiru!")
