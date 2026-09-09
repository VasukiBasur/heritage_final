import re

with open('templates/supplier_analytics.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove ALL badly injected downloadPDF blocks and closing divs that were prepended to EVERY endblock
bad_injection_pattern = r'</div>\n<script>\n    function downloadPDF\(\) \{.*?</script>\n'
text = re.sub(bad_injection_pattern, '', text, flags=re.DOTALL)

# Remove the stray closing div right before {% endblock %} if there's any left
text = re.sub(r'</div>\n{% endblock %}', '{% endblock %}', text)

# Remove any duplicate html2pdf cdns
text = re.sub(r'<!-- html2pdf CDN -->\n<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>', '', text)

# Re-inject cleanly
# 1. CDN inside block content
text = text.replace('{% block content %}', '{% block content %}\n<!-- html2pdf CDN -->\n<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>')

# 2. Add id=pdf-content wrapper correctly if not already present
text = text.replace('<div id="pdf-content">\n<div id="pdf-content">', '<div id="pdf-content">')
if '<div id="pdf-content">' not in text:
    text = text.replace('<!-- 1. HIGH LEVEL KPI CARDS -->', '<div id="pdf-content">\n<!-- 1. HIGH LEVEL KPI CARDS -->')

# 3. Add closing div and JS specifically AT THE VERY END OF THE FILE, which should be the content endblock.
parts = text.rsplit('{% endblock %}', 1)
js_code = '''
</div>
<script>
    function downloadPDF() {
        const element = document.getElementById('pdf-content');
        const opt = {
            margin:       0.5,
            filename:     'Supplier_Analytics_Report.pdf',
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, useCORS: true, backgroundColor: '#141414' },
            jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        alert("Generating Analytics PDF... Please wait.");
        html2pdf().set(opt).from(element).save();
    }
</script>
{% endblock %}'''

if len(parts) > 1:
    text = parts[0] + js_code + parts[1]

with open('templates/supplier_analytics.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Cleaned up supplier_analytics.html')
