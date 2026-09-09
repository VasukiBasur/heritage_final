import re

with open('templates/supplier_analytics.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Inject CDN script
if 'html2pdf' not in text:
    text = text.replace('{% block content %}', '{% block content %}\n<!-- html2pdf CDN -->\n<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>')

# 2. Update Export Button
btn_pattern = r'<button class="([^"]*)">\s*<svg[^>]*>.*?</svg>\s*Export Report\s*</button>'
btn_replace = r'<button onclick="downloadPDF()" class="\g<1>">\n            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>\n            Export Report\n        </button>'
text = re.sub(btn_pattern, btn_replace, text, flags=re.IGNORECASE | re.DOTALL)

# 3. Add id='pdf-content' to wrap the body
if 'id="pdf-content"' not in text:
    text = text.replace('<!-- 1. HIGH LEVEL KPI CARDS -->', '<div id="pdf-content">\n<!-- 1. HIGH LEVEL KPI CARDS -->')
    # Close it before the endblock
    text = text.replace('{% endblock %}', '</div>\n{% endblock %}')

# 4. Add downloadPDF() javascript
js_code = '''
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
'''
if 'function downloadPDF()' not in text:
    text = text.replace('{% endblock %}', js_code + '{% endblock %}')

with open('templates/supplier_analytics.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated supplier_analytics.html with PDF export.')
