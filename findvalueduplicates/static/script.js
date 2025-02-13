document.addEventListener('DOMContentLoaded', function() {
    const analyzeButton = document.getElementById('analyzeButton');
    const logInput = document.getElementById('logInput');
    const results = document.getElementById('results');
    const duplicateReport = document.getElementById('duplicateReport');

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

                    try {
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
                        
                        let reportHtml = '<h2>Duplicate Values Report</h2>';
                        
                        if (Object.keys(data).length === 0) {
                            reportHtml += '<p>No duplicates found in this line.</p>';
                        } else {
                            for (const [value, info] of Object.entries(data)) {
                                reportHtml += `
                                    <div class="duplicate-item">
                                        <div class="duplicate-value">Value: "${value}"</div>
                                        <div class="duplicate-count">Count: ${info.count}</div>
                                        <div class="duplicate-keys">Keys: ${info.keys.join(', ')}</div>
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