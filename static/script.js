document.addEventListener('DOMContentLoaded', function() {
    // API base URL - change this if your server is running on a different host/port
    const API_BASE_URL = '';  // Empty means same host as UI
    
    // Tab navigation
    const tabs = {
        'risk-analysis-tab': 'risk-analysis-section',
        'incident-log-tab': 'incident-log-section',
        'about-tab': 'about-section'
    };
    
    // Set up tab navigation
    Object.keys(tabs).forEach(tabId => {
        document.getElementById(tabId).addEventListener('click', function(e) {
            e.preventDefault();
            
            // Update active tab
            document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));
            this.classList.add('active');
            
            // Hide all sections
            document.querySelectorAll('.tab-section').forEach(el => {
                el.classList.add('fade-out');
                setTimeout(() => {
                    el.style.display = 'none';
                    el.classList.remove('fade-out');
                }, 300);
            });
            
            // Show selected section
            setTimeout(() => {
                document.getElementById(tabs[tabId]).style.display = 'block';
            }, 300);
        });
    });
    
    // Risk Analysis Form Submission
    document.getElementById('project-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const description = document.getElementById('project-description').value.trim();
        if (!description) {
            alert('Please enter a project description.');
            return;
        }
        
        // Show results section
        document.getElementById('results-section').style.display = 'block';
        
        // Show loading spinner and hide results
        document.getElementById('loading-spinner').style.display = 'block';
        document.getElementById('results-content').style.display = 'none';
        
        // Scroll to results
        document.getElementById('results-section').scrollIntoView({
            behavior: 'smooth'
        });
        
        // Call the API
        fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: description })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('API request failed');
            }
            return response.json();
        })
        .then(data => {
            // Hide loading spinner
            document.getElementById('loading-spinner').style.display = 'none';
            document.getElementById('results-content').style.display = 'block';
            
            // Display response
            displayResults(data, description);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('loading-spinner').style.display = 'none';
            document.getElementById('results-content').style.display = 'block';
            document.getElementById('agent-response').innerHTML = 
                `<div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    An error occurred while processing your request. Please try again.
                </div>`;
        });
    });
    
    // Incident Log Form Submission
    document.getElementById('incident-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const projectId = document.getElementById('project-id').value.trim();
        const incidentDate = document.getElementById('incident-date').value;
        const incidentType = document.getElementById('incident-type').value;
        const severity = document.getElementById('incident-severity').value;
        const description = document.getElementById('incident-description').value.trim();
        
        if (!projectId || !incidentDate || !incidentType || !severity || !description) {
            alert('Please fill in all fields.');
            return;
        }
        
        // In a real application, you would send this data to your API
        // For this demo, we'll just add it to the table
        const tbody = document.querySelector('#incidents-table tbody');
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${projectId}</td>
            <td>${incidentDate}</td>
            <td>${incidentType}</td>
            <td><span class="badge ${getBadgeClass(severity)}">${severity}</span></td>
            <td>${description}</td>
        `;
        
        tbody.prepend(row);
        
        // Reset form
        this.reset();
        
        // Show success message
        alert('Incident logged successfully!');
    });
    
    // Export PDF button
    document.getElementById('export-pdf-btn').addEventListener('click', function() {
        alert('PDF export functionality would be implemented here.');
        // In a real app, you would use a library like jsPDF or call a backend endpoint
    });
    
    // Check API status
    checkApiStatus();
    
    // Fetch system info
    fetchSystemInfo();
    
    // Helper Functions
    
    /**
     * Renders the analysis results
     */
    function displayResults(data, description) {
        // Display agent response
        document.getElementById('agent-response').innerText = data.response || 'No response from agent';
        
        // Extract risks from response (this is a simplified example)
        // In a real application, you might get structured data from the API
        // For this demo, we'll generate some mock risk data based on keywords in the response
        const riskData = analyzeResponseForRisks(data.response, description);
        
        // Populate risk table
        populateRiskTable(riskData);
        
        // Generate risk chart
        generateRiskChart(riskData);
    }
    
    /**
     * Checks the API status
     */
    function checkApiStatus() {
        const statusElement = document.getElementById('api-status');
        
        fetch(`${API_BASE_URL}/health`)
            .then(response => {
                if (!response.ok) throw new Error('API is not available');
                return response.json();
            })
            .then(data => {
                if (data.status === 'healthy') {
                    statusElement.innerHTML = '<i class="fas fa-check-circle text-success me-2"></i>Online';
                } else {
                    statusElement.innerHTML = '<i class="fas fa-exclamation-circle text-warning me-2"></i>Degraded';
                }
            })
            .catch(error => {
                console.error('Error checking API status:', error);
                statusElement.innerHTML = '<i class="fas fa-times-circle text-danger me-2"></i>Offline';
            });
    }
    
    /**
     * Fetches system information
     */
    function fetchSystemInfo() {
        const versionElement = document.getElementById('system-version');
        
        fetch(`${API_BASE_URL}/info`)
            .then(response => {
                if (!response.ok) throw new Error('Could not fetch system info');
                return response.json();
            })
            .then(data => {
                versionElement.textContent = data.version || 'Unknown';
            })
            .catch(error => {
                console.error('Error fetching system info:', error);
                versionElement.textContent = 'Unavailable';
            });
    }
    
    /**
     * Analyzes the response for risks (mock implementation)
     */
    function analyzeResponseForRisks(response, description) {
        // This is a simplified mock implementation
        // In a real app, your API would likely return structured risk data
        
        const riskTypes = {
            'Safety': detectRiskLevel(response, description, ['safety', 'injury', 'accident', 'hazard', 'danger']),
            'Delay': detectRiskLevel(response, description, ['delay', 'timeline', 'schedule', 'late', 'postpone']),
            'Budget Overrun': detectRiskLevel(response, description, ['budget', 'cost', 'expense', 'financial', 'overrun']),
            'Quality Issue': detectRiskLevel(response, description, ['quality', 'defect', 'standard', 'specification']),
            'Environmental': detectRiskLevel(response, description, ['environment', 'pollution', 'waste', 'contamination'])
        };
        
        // Generate mock mitigation strategies
        const mitigationStrategies = {
            'Safety': 'Implement regular safety training and inspections. Use proper PPE at all times.',
            'Delay': 'Create a detailed project schedule with buffer time. Monitor critical path activities closely.',
            'Budget Overrun': 'Maintain a contingency fund of 15-20%. Conduct weekly financial reviews.',
            'Quality Issue': 'Implement quality control checkpoints. Use third-party inspections at key milestones.',
            'Environmental': 'Follow environmental regulations. Implement waste management plan and monitoring.'
        };
        
        const result = [];
        for (const [riskType, level] of Object.entries(riskTypes)) {
            result.push({
                type: riskType,
                level: level,
                levelValue: getRiskLevelValue(level),
                mitigation: mitigationStrategies[riskType]
            });
        }
        
        return result;
    }
    
    /**
     * Detects risk level based on keywords (mock implementation)
     */
    function detectRiskLevel(response, description, keywords) {
        const combinedText = (response + ' ' + description).toLowerCase();
        let count = 0;
        
        keywords.forEach(keyword => {
            const regex = new RegExp('\\b' + keyword + '\\b', 'gi');
            const matches = combinedText.match(regex);
            if (matches) {
                count += matches.length;
            }
        });
        
        if (count >= 4) return 'Critical';
        if (count >= 2) return 'High';
        if (count >= 1) return 'Medium';
        return 'Low';
    }
    
    /**
     * Gets the numeric value for a risk level
     */
    function getRiskLevelValue(level) {
        switch (level) {
            case 'Critical': return 0.9;
            case 'High': return 0.7;
            case 'Medium': return 0.4;
            case 'Low': return 0.2;
            default: return 0;
        }
    }
    
    /**
     * Populates the risk table with data
     */
    function populateRiskTable(riskData) {
        const tbody = document.querySelector('#risks-table tbody');
        tbody.innerHTML = '';
        
        riskData.forEach(risk => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${risk.type}</td>
                <td><span class="badge ${getBadgeClass(risk.level)}">${risk.level}</span></td>
                <td>${risk.mitigation}</td>
            `;
            tbody.appendChild(row);
        });
    }
    
    /**
     * Generates a chart for risk visualization
     */
    function generateRiskChart(riskData) {
        const ctx = document.getElementById('risk-visualization');
        
        // Clear any existing chart
        if (window.riskChart) {
            window.riskChart.destroy();
        }
        
        // Prepare data
        const labels = riskData.map(r => r.type);
        const data = riskData.map(r => r.levelValue * 100);
        const backgroundColors = riskData.map(r => {
            switch (r.level) {
                case 'Critical': return 'rgba(220, 53, 69, 0.7)';
                case 'High': return 'rgba(253, 126, 20, 0.7)';
                case 'Medium': return 'rgba(255, 193, 7, 0.7)';
                case 'Low': return 'rgba(25, 135, 84, 0.7)';
                default: return 'rgba(173, 181, 189, 0.7)';
            }
        });
        
        // Create chart
        window.riskChart = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Risk Level (%)',
                    data: data,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgb(54, 162, 235)',
                    pointBackgroundColor: backgroundColors,
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: backgroundColors
                }]
            },
            options: {
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            display: false
                        }
                    }
                }
            }
        });
        
        // If it's a div, set its innerHTML to have a canvas
        if (ctx.tagName === 'DIV') {
            ctx.innerHTML = '<canvas id="risk-chart"></canvas>';
            const canvas = document.getElementById('risk-chart');
            window.riskChart = new Chart(canvas, { /* same config */ });
        }
    }
    
    /**
     * Returns the appropriate Bootstrap badge class for a risk level
     */
    function getBadgeClass(level) {
        switch (level) {
            case 'Critical': return 'bg-danger';
            case 'High': return 'bg-warning text-dark';
            case 'Medium': return 'bg-info text-dark';
            case 'Low': return 'bg-success';
            default: return 'bg-secondary';
        }
    }
});