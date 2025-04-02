frappe.ready(function() {
    // Initialize dashboard functionality
    const dashboard = {
        init: function() {
            this.setupEventListeners();
            this.refreshStats();
        },

        setupEventListeners: function() {
            // Add any click handlers or other event listeners
        },

        refreshStats: function() {
            // Refresh dashboard statistics periodically
            setInterval(() => {
                frappe.call({
                    method: 'frappe.client.get_count',
                    args: {
                        doctype: 'Property',
                        filters: {}
                    },
                    callback: function(r) {
                        if (!r.exc) {
                            $('.property-count').text(r.message || 0);
                        }
                    }
                });
            }, 60000); // Refresh every minute
        }
    };

    // Initialize the dashboard
    dashboard.init();
});