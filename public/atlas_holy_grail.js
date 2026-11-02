document.addEventListener('DOMContentLoaded', () => {
    const navButtons = document.querySelectorAll('.right-nav button');
    const tabContents = document.querySelectorAll('.tab-page');
    
    // Set initial theme to the active tab's theme
    const activeBtn = document.querySelector('.right-nav button.active');
    if(activeBtn) {
        document.body.className = activeBtn.getAttribute('data-theme');
    }

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all nav buttons
            navButtons.forEach(b => b.classList.remove('active'));
            
            // Hide all tab contents
            tabContents.forEach(tab => tab.classList.remove('active'));
            
            // Add active class to clicked button
            btn.classList.add('active');
            
            // Show corresponding tab content
            const targetId = btn.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
            
            // Change body theme class for dynamic background & colors
            const themeClass = btn.getAttribute('data-theme');
            document.body.className = themeClass;
            
            // Special Animation Triggers
            if (targetId === 'finance-tab') {
                const liquid = document.querySelector('.jar-liquid');
                if (liquid) {
                    liquid.style.height = '0%';
                    setTimeout(() => {
                        liquid.style.height = '1%';
                    }, 500);
                }
            }
        });
    });
});
