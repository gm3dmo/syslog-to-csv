document.addEventListener('DOMContentLoaded', function() {
    const analyzeButton = document.getElementById('analyzeButton');
    const logInput = document.getElementById('logInput');
    const results = document.getElementById('results');
    const duplicateReport = document.getElementById('duplicateReport');

    // Helper function to get the appropriate icon
    const getCountIcon = (count) => {
        const numCount = parseInt(count, 10);
        console.log('Count value:', numCount); // Debug log
        if (numCount > 1) {
            return `<span style="color: var(--govuk-red); font-weight: bold; margin-right: 5px;">❌</span>`;
        }
        return `<span style="color: var(--govuk-green); font-weight: bold; margin-right: 5px;">✅</span>`;
    };

    analyzeButton.addEventListener('click', function() {
        const logText = logInput.value.trim();
        if (logText) {
            results.style.display = 'block';
            
            // Split into lines and create numbered display
            const lines = logText.split('\n');
            const formattedLines = lines.map((line, index) => 
                `<div class="log-line" data-line-number="${index + 1}">
                    <span class="line-number">${index + 1}</span>
                    <span class="line-content">${line}</span>
                 </div>`
            ).join('');
            
            results.innerHTML = `<div class="log-container">${formattedLines}</div>`;

            // Add click handlers for lines
            document.querySelectorAll('.log-line').forEach(line => {
                line.addEventListener('click', async function() {
                    try {
                        // Remove highlight from all lines
                        document.querySelectorAll('.log-line').forEach(l => 
                            l.classList.remove('highlighted'));
                        // Add highlight to clicked line
                        this.classList.add('highlighted');
                        
                        // Get the line content and analyze it
                        const lineContent = this.querySelector('.line-content').textContent;
                        console.log('Sending line for analysis:', lineContent);
                        
                        duplicateReport.innerHTML = '<h2>Duplicate Values Report</h2><p>Analyzing...</p>';
                        duplicateReport.style.display = 'block';

                        const response = await fetch('/analyze', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ line: lineContent })
                        });
                        
                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }
                        
                        const data = await response.json();
                        console.log('Analysis result:', data);

                        if (data.error) {
                            throw new Error(data.error);
                        }
                        
                        let reportHtml = '<h2>Duplicate Values Report</h2>';
                        
                        if (!data || Object.keys(data).length === 0) {
                            reportHtml += '<p>No duplicates found in this line.</p>';
                        } else {
                            const summary = data._summary || {};
                            const entries = Object.entries(data).filter(([key]) => key !== '_summary');
                            
                            for (const [value, info] of entries) {
                                if (info && Array.isArray(info.keys)) {
                                    const count = info.count || 0;
                                    console.log('Processing count:', count); // Debug log
                                    reportHtml += `
                                        <div class="duplicate-item">
                                            <div class="duplicate-value">Value: "${value}"</div>
                                            <div class="duplicate-count">${getCountIcon(count)}Count: ${count}</div>
                                            <div class="duplicate-keys">Keys: ${info.keys.join(', ')}</div>
                                            <div class="bytes-duplicated">Bytes duplicated: ${info.bytes_duplicated || 0}</div>
                                        </div>
                                    `;
                                }
                            }
                            
                            if (summary && typeof summary.total_bytes_duplicated !== 'undefined') {
                                reportHtml += `
                                    <div class="total-bytes">
                                        <strong>Total Bytes Duplicated: ${summary.total_bytes_duplicated}</strong>
                                    </div>
                                `;
                            }
                        }
                        
                        duplicateReport.innerHTML = reportHtml;
                        
                    } catch (error) {
                        console.error('Error during analysis:', error);
                        duplicateReport.innerHTML = `
                            <h2>Duplicate Values Report</h2>
                            <p>Error analyzing line: ${error.message}</p>
                        `;
                    }
                });
            });
        } else {
            results.style.display = 'none';
            duplicateReport.style.display = 'none';
        }
    });
}); 