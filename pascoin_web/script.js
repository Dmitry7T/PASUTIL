document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('nav a[href^="#"], .hero-cta a[href^="#"], .about-text a[href^="#"], .footer-nav a[href^="#"], .footer-legal a[href^="#"], .footer-contact a[href^="#"], .section-header a[href^="#"], .cta-button[href^="#"], .btn-primary[href^="#"], .btn-secondary[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

});


