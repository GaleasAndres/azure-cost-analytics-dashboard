// Azure Cost Analytics Dashboard - Frontend Application

class AzureCostDashboard {
    constructor() {
        this.currentSubscription = null;
        this.isAuthenticated = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuthenticationStatus();
        this.loadSubscriptions();
    }

    setupEventListeners() {
        // Login button
        const loginBtn = document.getElementById('login-btn');
        if (loginBtn) {
            loginBtn.addEventListener('click', () => {
                window.location.href = '/auth/login';
            });
        }

        // Logout button
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                window.location.href = '/auth/logout';
            });
        }

        // Subscription selector
        const subscriptionSelect = document.getElementById('subscription-select');
        if (subscriptionSelect) {
            subscriptionSelect.addEventListener('change', (e) => {
                this.currentSubscription = e.target.value;
                if (this.currentSubscription) {
                    this.loadDashboardData();
                }
            });
        }
    }

    async checkAuthenticationStatus() {
        try {
            const response = await fetch('/api/auth/status');
            if (response.ok) {
                const data = await response.json();
                this.isAuthenticated = data.authenticated;
                this.updateAuthUI(data.user);
            }
        } catch (error) {
            console.log('Not authenticated or server not running');
        }
    }

    updateAuthUI(user = null) {
        const loginBtn = document.getElementById('login-btn');
        const userInfo = document.getElementById('user-info');
        const userName = document.getElementById('user-name');

        if (this.isAuthenticated) {
            loginBtn.classList.add('hidden');
            userInfo.classList.remove('hidden');
            if (user && user.name) {
                userName.textContent = user.name;
            } else {
                userName.textContent = 'Azure User';
            }
        } else {
            loginBtn.classList.remove('hidden');
            userInfo.classList.add('hidden');
        }
    }

    async loadSubscriptions() {
        try {
            this.showLoading(true);
            const response = await fetch('/api/subscriptions');
            const data = await response.json();

            if (response.ok && data.subscriptions) {
                this.populateSubscriptionSelect(data.subscriptions);
            } else {
                this.showError('Failed to load subscriptions');
            }
        } catch (error) {
            console.error('Error loading subscriptions:', error);
            this.showError('Failed to load subscriptions');
        } finally {
            this.showLoading(false);
        }
    }

    populateSubscriptionSelect(subscriptions) {
        const select = document.getElementById('subscription-select');
        select.innerHTML = '<option value="">Select a subscription...</option>';
        
        subscriptions.forEach(sub => {
            const option = document.createElement('option');
            option.value = sub.subscription_id;
            option.textContent = `${sub.display_name} (${sub.state})`;
            select.appendChild(option);
        });
    }

    async loadDashboardData() {
        if (!this.currentSubscription) return;

        try {
            this.showLoading(true);
            
            // Load cost summary
            await this.loadCostSummary();
            
            // Load resource group costs
            await this.loadResourceGroupCosts();
            
            // Load resource groups list
            await this.loadResourceGroupsList();
            
            // Load daily costs chart
            await this.loadDailyCostsChart();
            
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showError('Failed to load dashboard data');
        } finally {
            this.showLoading(false);
        }
    }

    async loadCostSummary() {
        try {
            const response = await fetch(`/api/costs/summary?subscription_id=${this.currentSubscription}`);
            const data = await response.json();

            if (response.ok && data) {
                this.updateCostSummary(data);
            } else {
                this.showError('Failed to load cost summary');
            }
        } catch (error) {
            console.error('Error loading cost summary:', error);
        }
    }

    updateCostSummary(data) {
        const totalCost = document.getElementById('total-cost');
        const avgDailyCost = document.getElementById('avg-daily-cost');
        const periodDays = document.getElementById('period-days');

        if (totalCost) totalCost.textContent = `$${data.total_cost.toFixed(2)}`;
        if (avgDailyCost) avgDailyCost.textContent = `$${data.avg_daily_cost.toFixed(2)}`;
        if (periodDays) periodDays.textContent = `${data.period_days} days`;
    }

    async loadResourceGroupCosts() {
        try {
            const response = await fetch(`/api/costs/by-resource-group?subscription_id=${this.currentSubscription}`);
            const data = await response.json();

            if (response.ok && data.costs) {
                this.updateResourceGroupCosts(data.costs);
            } else {
                this.showError('Failed to load resource group costs');
            }
        } catch (error) {
            console.error('Error loading resource group costs:', error);
        }
    }

    updateResourceGroupCosts(costs) {
        const container = document.getElementById('resource-groups-list');
        if (!container) return;

        // Group costs by resource group
        const groupedCosts = {};
        costs.forEach(cost => {
            const rgName = cost.resource_group || 'Unknown';
            if (!groupedCosts[rgName]) {
                groupedCosts[rgName] = 0;
            }
            groupedCosts[rgName] += parseFloat(cost.cost || 0);
        });

        // Sort by cost (highest first)
        const sortedGroups = Object.entries(groupedCosts)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 10); // Show top 10

        container.innerHTML = '';
        
        if (sortedGroups.length === 0) {
            container.innerHTML = '<div class="loading">No cost data available</div>';
            return;
        }

        sortedGroups.forEach(([rgName, totalCost]) => {
            const item = document.createElement('div');
            item.className = 'resource-group-item';
            item.innerHTML = `
                <span class="resource-group-name">${rgName}</span>
                <span class="resource-group-cost">$${totalCost.toFixed(2)}</span>
            `;
            container.appendChild(item);
        });
    }

    async loadResourceGroupsList() {
        try {
            const response = await fetch(`/api/resource-groups?subscription_id=${this.currentSubscription}`);
            const data = await response.json();

            if (response.ok && data.resource_groups) {
                this.updateResourceGroupsTable(data.resource_groups);
            } else {
                this.showError('Failed to load resource groups');
            }
        } catch (error) {
            console.error('Error loading resource groups:', error);
        }
    }

    updateResourceGroupsTable(resourceGroups) {
        const container = document.getElementById('resource-groups-table');
        if (!container) return;

        if (resourceGroups.length === 0) {
            container.innerHTML = '<div class="loading">No resource groups found</div>';
            return;
        }

        const table = document.createElement('table');
        table.className = 'resource-groups-table';
        
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Location</th>
                    <th>ID</th>
                </tr>
            </thead>
            <tbody>
                ${resourceGroups.map(rg => `
                    <tr>
                        <td>${rg.name}</td>
                        <td>${rg.location}</td>
                        <td style="font-size: 0.8em; color: #718096;">${rg.id}</td>
                    </tr>
                `).join('')}
            </tbody>
        `;

        container.innerHTML = '';
        container.appendChild(table);
    }

    async loadDailyCostsChart() {
        try {
            const response = await fetch(`/api/costs/last-month?subscription_id=${this.currentSubscription}`);
            const data = await response.json();

            if (response.ok && data.costs) {
                this.updateDailyCostsChart(data.costs);
            } else {
                this.showError('Failed to load daily costs');
            }
        } catch (error) {
            console.error('Error loading daily costs:', error);
        }
    }

    updateDailyCostsChart(costs) {
        const container = document.getElementById('daily-costs-chart');
        if (!container) return;

        if (costs.length === 0) {
            container.innerHTML = '<div class="loading">No daily cost data available</div>';
            return;
        }

        // Create a simple bar chart using CSS
        const chartData = costs.slice(-10); // Last 10 days
        
        container.innerHTML = `
            <div class="simple-chart">
                <div class="chart-bars">
                    ${chartData.map(cost => {
                        const costValue = parseFloat(cost.Cost || 0);
                        const maxCost = Math.max(...chartData.map(c => parseFloat(c.Cost || 0)));
                        const height = maxCost > 0 ? (costValue / maxCost) * 100 : 0;
                        const date = new Date(cost.UsageDate).toLocaleDateString('en-US', { 
                            month: 'short', 
                            day: 'numeric' 
                        });
                        
                        return `
                            <div class="chart-bar">
                                <div class="bar" style="height: ${height}%"></div>
                                <div class="bar-label">${date}</div>
                                <div class="bar-value">$${costValue.toFixed(2)}</div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    }

    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.toggle('hidden', !show);
        }
    }

    showError(message) {
        console.error(message);
        // In a real app, you'd show this in the UI
        alert(message);
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new AzureCostDashboard();
});

// Add CSS for the simple chart
const chartStyles = `
<style>
.simple-chart {
    width: 100%;
    height: 200px;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding: 1rem 0;
}

.chart-bars {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    width: 100%;
    height: 100%;
    gap: 4px;
}

.chart-bar {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    height: 100%;
    position: relative;
}

.bar {
    width: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 4px 4px 0 0;
    min-height: 4px;
    transition: all 0.3s ease;
}

.bar:hover {
    background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    transform: scaleY(1.1);
}

.bar-label {
    font-size: 0.75rem;
    color: #718096;
    margin-top: 0.5rem;
    text-align: center;
}

.bar-value {
    font-size: 0.7rem;
    color: #4a5568;
    font-weight: 500;
    margin-top: 0.25rem;
    text-align: center;
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', chartStyles);
