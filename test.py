with open('templates/result.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Show exactly what's around the summary marker
idx = content.find('<!-- AI CLINICAL SUMMARY -->')
print("=== AROUND SUMMARY MARKER ===")
print(repr(content[idx-50:idx+80]))
print()

# Show exactly what's around the recs marker  
idx2 = content.find('<!-- AI CLINICAL RECOMMENDATIONS -->')
print("=== AROUND RECS MARKER ===")
print(repr(content[idx2-50:idx2+80]))
print()

# Show exactly what's around the button
idx3 = content.find('openAIPanel')
print("=== AROUND BUTTON ===")
print(repr(content[idx3-100:idx3+60]))