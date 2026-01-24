/**
 * Counter Animation - Smooth number counting when scrolled into view
 * Usage: Add class "count-up" to elements with numbers
 * Supports: $1.6B, 519+, 60%+, 135K, 2,000, plain numbers
 */

(function() {
    'use strict';

    // Parse number from text (handles $, B, K, M, %, +, commas)
    function parseNumber(text) {
        const cleaned = text.replace(/[$,+%BMK]/gi, '').trim();
        return parseFloat(cleaned) || 0;
    }

    // Get the format parts (prefix, suffix, decimals)
    function getFormat(text) {
        const prefix = text.match(/^[$]/) ? '$' : '';
        const suffix = text.match(/[BMK%+]+$/i) ? text.match(/[BMK%+]+$/i)[0] : '';
        const hasComma = text.includes(',');
        const decimals = text.includes('.') ? (text.split('.')[1].match(/\d+/) || [''])[0].length : 0;
        return { prefix, suffix, hasComma, decimals };
    }

    // Format number back to original style
    function formatNumber(num, format) {
        let result = format.decimals > 0
            ? num.toFixed(format.decimals)
            : Math.round(num).toString();

        if (format.hasComma) {
            result = result.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        }

        return format.prefix + result + format.suffix;
    }

    // Easing function for smooth animation
    function easeOutQuart(t) {
        return 1 - Math.pow(1 - t, 4);
    }

    // Animate a single counter
    function animateCounter(element) {
        if (element.dataset.animated) return;
        element.dataset.animated = 'true';

        const originalText = element.textContent.trim();
        const targetNum = parseNumber(originalText);
        const format = getFormat(originalText);
        const duration = 1500; // 1.5 seconds
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easedProgress = easeOutQuart(progress);
            const currentNum = targetNum * easedProgress;

            element.textContent = formatNumber(currentNum, format);

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        // Start from 0
        element.textContent = formatNumber(0, format);
        requestAnimationFrame(update);
    }

    // Intersection Observer for scroll trigger
    function initCounters() {
        const counters = document.querySelectorAll('.count-up');

        if (!counters.length) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.3,
            rootMargin: '0px 0px -50px 0px'
        });

        counters.forEach(counter => observer.observe(counter));
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCounters);
    } else {
        initCounters();
    }
})();
