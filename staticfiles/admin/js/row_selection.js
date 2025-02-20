document.addEventListener('DOMContentLoaded', function() {
    // Function to toggle checkbox
    function toggleCheckbox(tr) {
        const checkbox = tr.querySelector('input.action-select');
        if (checkbox) {
            checkbox.checked = !checkbox.checked;
            // Trigger change event to update UI
            checkbox.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }

    // Handle row clicks
    document.querySelectorAll('#result_list tbody tr').forEach(tr => {
        tr.style.cursor = 'pointer';
        tr.addEventListener('click', function(e) {
            // Don't toggle if clicking on a link or checkbox
            if (e.target.tagName === 'A' || e.target.tagName === 'INPUT') {
                return;
            }
            toggleCheckbox(this);
        });
    });

    // Handle name column clicks
    document.querySelectorAll('.row-selector').forEach(selector => {
        selector.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const tr = this.closest('tr');
            toggleCheckbox(tr);
        });
    });
}); 