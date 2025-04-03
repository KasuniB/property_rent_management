frappe.provide('property_rent_management');

property_rent_management = {
    init() {
        // Initialize app features
        this.setupDashboard();
        this.setupEventHandlers();
    },

    setupDashboard() {
        // Dashboard initialization
        if (frappe.pages['property-rent-management']) {
            this.initializeDashboardCharts();
            this.loadPropertyList();
        }
    },

    setupEventHandlers() {
        // Setup global event handlers
        $(document).on('property_rent_management.update', () => {
            this.refreshDashboard();
        });
    },

    initializeDashboardCharts() {
        // Initialize dashboard charts
        if (!frappe.boot.property_rent_stats) return;
        
        // Render charts using frappe.Chart
        new frappe.Chart('#property-stats', {
            data: frappe.boot.property_rent_stats,
            type: 'bar',
            height: 250
        });
    },

    loadPropertyList() {
        // Load property list
        frappe.call({
            method: 'property_rent_management.api.get_property_list',
            callback: (r) => {
                if (r.message) {
                    this.renderPropertyList(r.message);
                }
            }
        });
    },

    refreshDashboard() {
        // Refresh dashboard data
        this.loadPropertyList();
        this.initializeDashboardCharts();
    }
};

// Initialize on page load
$(document).ready(() => {
    property_rent_management.init();
});
