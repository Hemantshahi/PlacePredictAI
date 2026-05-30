/**
 * PlacePredict AI — MCE T&P Cell
 * main.js — Common Frontend Logic
 */

'use strict';

// ── Auto-dismiss flash alerts ──────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.querySelectorAll('.alert.fade.show').forEach(el => {
            const alert = bootstrap.Alert.getOrCreateInstance(el);
            alert.close();
        });
    }, 5000);

    // ── Progress bar animate on scroll ──────────────────────
    const observeProgress = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.querySelectorAll('.progress-bar[style*="width"]').forEach(bar => {
                    const width = bar.style.width;
                    bar.style.width = '0%';
                    requestAnimationFrame(() => {
                        setTimeout(() => { bar.style.width = width; }, 50);
                    });
                });
            }
        });
    }, { threshold: 0.2 });

    document.querySelectorAll('.dash-card, .ats-breakdown, .model-scores').forEach(el => {
        observeProgress.observe(el);
    });

    // ── Active nav link highlight ─────────────────────────── 
    const currentPath = window.location.pathname;
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        if (link.getAttribute('href') && currentPath.startsWith(link.getAttribute('href')) && link.getAttribute('href') !== '/') {
            link.classList.add('active');
            link.style.color = '#e2e8f0 !important';
        }
    });
});
