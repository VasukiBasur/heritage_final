import re

with open('templates/supplier_analytics.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove ALL badly injected downloadPDF blocks and closing divs
# The \s* matches any whitespace including newlines
bad_injection_pattern = r'</div>\s*<script>\s*function downloadPDF\(\) \{.*?</script>'
text = re.sub(bad_injection_pattern, '', text, flags=re.DOTALL)

# Ensure the final block is correct
# We know the JS at the very end of the file is correct, so we shouldn't strip the last one if it's placed right.
# Wait, my regex stripped ALL of them, including the good one at the end!
# That's fine, I'll just append the good one back.

text = re.sub(r'</div>\s*{% endblock %}', '{% endblock %}', text)

# Re-add the closing div and JS specifically AT THE VERY END OF THE FILE, which should be the content endblock.
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

print('Cleaned up supplier_analytics.html robustly')
