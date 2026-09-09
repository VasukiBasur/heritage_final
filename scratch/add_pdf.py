import re

with open('templates/supplier_earnings.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add html2pdf CDN
cdn_block = """<!-- Chart.js CDN -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<!-- html2pdf CDN -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>"""

text = text.replace('<!-- Chart.js CDN -->\n<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>', cdn_block)

# 2. Add an ID to the button and hook it
btn_old = """<button class="bg-gradient-to-r from-[#d4af37] to-[#b8860b] text-black text-xs font-bold uppercase tracking-widest py-3 px-6 rounded-md shadow-[0_0_15px_rgba(212,175,55,0.4)] hover:brightness-110 transition-all">
            DOWNLOAD REPORT (PDF)
        </button>"""
btn_new = """<button onclick="downloadPDF()" class="bg-gradient-to-r from-[#d4af37] to-[#b8860b] text-black text-xs font-bold uppercase tracking-widest py-3 px-6 rounded-md shadow-[0_0_15px_rgba(212,175,55,0.4)] hover:brightness-110 transition-all">
            DOWNLOAD REPORT (PDF)
        </button>"""
text = text.replace(btn_old, btn_new)

# 3. Add an ID to the content container to capture it
# Find the first grid or something that holds the charts
# Wait, let's just wrap the entire content after the header in a div
wrap_start = "<!-- KPI Cards -->"
wrap_end = "<!-- Main Chart & Transactions -->"
# Actually let's just wrap everything from KPI cards to the end of the transactions block
text = text.replace("<!-- KPI Cards -->", '<div id="pdf-content">\n<!-- KPI Cards -->')
text = text.replace("<!-- End Chart -->", "<!-- End Chart -->\n</div>")
# Wait, let's just use JS to target the main block content instead of injecting a div, 
# wait, it's safer to just target the `main` or the top level content wrapper if it exists.
# Let's write the JS to target `document.querySelector('.ml-64.p-8')` if it exists, or just we can add the ID manually.

# 4. Add the javascript logic
js_block = """
    function downloadPDF() {
        const element = document.getElementById('pdf-content');
        
        // Add a temporary background to ensure dark mode renders correctly in PDF
        const opt = {
            margin:       0.5,
            filename:     'Heritage_Earnings_Report.pdf',
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, useCORS: true, backgroundColor: '#141414' },
            jsPDF:        { unit: 'in', format: 'letter', orientation: 'landscape' }
        };

        // Output toast to user
        alert("Generating PDF... Please wait.");
        html2pdf().set(opt).from(element).save();
    }
"""
text = text.replace('</script>\n{% endblock %}', js_block + '</script>\n{% endblock %}')

with open('templates/supplier_earnings.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Added PDF download functionality.')
