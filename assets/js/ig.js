// SeamlessFlow site behavior. Shared by every page; each block checks that its elements exist.
(function () {
    var A = document.documentElement.getAttribute('data-a') || 'assets/';
    var $ = function (s) { return document.querySelector(s); }, $$ = function (s) { return [].slice.call(document.querySelectorAll(s)); };

    // Text links open Messages on a phone; on a computer they go to the contact page instead.
    var mob = /Android|iPhone|iPad|iPod|Mobi/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    $$('a[href^="sms:"]').forEach(function (a) {
        if (!mob) a.setAttribute('href', 'book-call.html#contact');
        a.addEventListener('click', function () { if (typeof gtag !== 'undefined') gtag('event', 'text_click', { event_category: 'engagement' }); });
    });

    // Videos load and play only while on screen. Skipped for reduced-motion and data-saver.
    var calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches || (navigator.connection && navigator.connection.saveData);
    function play(v) { if (calm) return; if (!v.getAttribute('src') && v.dataset.src) v.src = v.dataset.src; var p = v.play(); if (p) p.catch(function () {}); }
    if ('IntersectionObserver' in window) {
        var vio = new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? play(e.target) : e.target.pause(); }); }, { threshold: 0.25 });
        $$('.feed-vid').forEach(function (v) { vio.observe(v); });
    }

    // Dialogs: click the dark area to close. More menu.
    $$('dialog').forEach(function (d) { d.addEventListener('click', function (e) { if (e.target === d) d.close(); }); });
    var menu = $('#menu');
    if (menu) {
        $$('[data-menu]').forEach(function (b) { b.addEventListener('click', function () { menu.showModal(); }); });
        menu.querySelector('[data-close]').addEventListener('click', function () { menu.close(); });
    }

    // Share, save, and a small toast to confirm what happened.
    var toastEl, toastT;
    function toast(msg) {
        if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'toast'; toastEl.setAttribute('role', 'status'); document.body.appendChild(toastEl); }
        toastEl.textContent = msg; toastEl.classList.add('show');
        clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove('show'); }, 3200);
    }
    var siteUrl = 'https://seamlessflow.ai/';
    $$('[data-share]').forEach(function (b) {
        b.addEventListener('click', function () {
            var data = { title: 'SeamlessFlow', text: 'Check out SeamlessFlow, they make content for local businesses.', url: siteUrl };
            if (navigator.share) { navigator.share(data).catch(function () {}); return; }
            if (navigator.clipboard) navigator.clipboard.writeText(siteUrl).then(function () { toast('Link copied. Send it to someone.'); }, function () { toast(siteUrl); });
            else toast(siteUrl);
        });
    });
    // Websites can't add a bookmark for you, so the save button says how.
    var ios = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    var android = /Android/.test(navigator.userAgent), mac = /Mac/.test(navigator.platform);
    var saveTip = ios ? 'tap Share, then "Add to Home Screen".' : android ? 'tap ⋮ in your browser, then the star.' : 'press ' + (mac ? '⌘' : 'Ctrl') + '+D.';
    $$('[data-save]').forEach(function (b) {
        b.addEventListener('click', function () {
            var on = !b.classList.contains('on');
            $$('[data-save]').forEach(function (x) { x.classList.toggle('on', on); x.setAttribute('aria-pressed', on); });
            if (!on) return;
            toast('To save us: ' + saveTip);
        });
    });

    // Likes: tap the heart, or double-tap the picture.
    $$('.post').forEach(function (post) {
        var like = post.querySelector('.like'), media = post.querySelector('.media, .car-wrap, .post-card'), last = 0;
        if (!like) return;
        function set(on) {
            like.classList.toggle('on', on); like.setAttribute('aria-pressed', on);
            // First like of the visit: one playful nudge to keep us close. Never again that visit.
            if (on && !sessionStorage.getItem('sf-liked')) {
                sessionStorage.setItem('sf-liked', '1');
                setTimeout(function () { toast('Liking us already? Keep us one tap away: ' + saveTip); }, 500);
            }
        }
        like.addEventListener('click', function () { set(!like.classList.contains('on')); });
        if (media) media.addEventListener('click', function (e) {
            if (e.target.closest('button, a')) return;
            var now = Date.now();
            if (now - last < 320) {
                set(true);
                if (getComputedStyle(media).position === 'static') media.style.position = 'relative';
                var h = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                h.setAttribute('class', 'ic heart-pop'); h.innerHTML = '<use href="#i-heart"/>';
                media.appendChild(h); setTimeout(function () { h.remove(); }, 850);
            }
            last = now;
        });
    });

    // Carousels: dots, counter and arrows follow the swipe.
    $$('.car-wrap').forEach(function (w) {
        var car = w.querySelector('.car'), n = car.children.length, count = w.querySelector('.count'), dots = [].slice.call(w.parentNode.querySelectorAll('.dots i')), prev = w.querySelector('.prev'), next = w.querySelector('.next'), tiers = [].slice.call(w.parentNode.querySelectorAll('.tiers button')), tick = 0;
        function sync() {
            var i = Math.round(car.scrollLeft / car.clientWidth);
            count.textContent = (i + 1) + '/' + n;
            dots.forEach(function (d, k) { d.classList.toggle('on', k === i); });
            tiers.forEach(function (t, k) { t.classList.toggle('on', k === i); });
            prev.disabled = i === 0; next.disabled = i === n - 1;
        }
        car.addEventListener('scroll', function () { cancelAnimationFrame(tick); tick = requestAnimationFrame(sync); });
        prev.addEventListener('click', function () { car.scrollBy({ left: -car.clientWidth, behavior: calm ? 'auto' : 'smooth' }); });
        next.addEventListener('click', function () { car.scrollBy({ left: car.clientWidth, behavior: calm ? 'auto' : 'smooth' }); });
        tiers.forEach(function (t, k) { t.addEventListener('click', function () { car.scrollTo({ left: k * car.clientWidth, behavior: calm ? 'auto' : 'smooth' }); }); });
        sync();
    });

    // FAQ: type to search, tap a chip to filter by topic.
    var fq = $('#faq-q');
    if (fq) {
        var groups = $$('.faq-g'), chips = $$('.chips button'), none = $('.faq-none'), g = 'all';
        function filter() {
            var q = fq.value.trim().toLowerCase(), shown = 0;
            groups.forEach(function (sec) {
                var n = 0, ok = g === 'all' || sec.dataset.g === g;
                [].forEach.call(sec.querySelectorAll('.faq > li'), function (li) {
                    var hit = ok && (!q || li.textContent.toLowerCase().indexOf(q) > -1);
                    li.hidden = !hit; if (hit) n++;
                    if (q) li.querySelector('details').open = hit && q.length > 2;
                });
                sec.hidden = !n; shown += n;
            });
            none.hidden = shown > 0;
        }
        fq.addEventListener('input', filter);
        chips.forEach(function (c) { c.addEventListener('click', function () {
            g = c.dataset.g; chips.forEach(function (x) { x.classList.toggle('on', x === c); x.setAttribute('aria-pressed', x === c); }); filter();
        }); });
    }

    // Contact form: sends through Web3Forms; falls back to an email draft until the key is set.
    var form = $('#contact-form'), st = $('#cf-status');
    if (form) form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (form.access_key.value === 'WEB3FORMS_ACCESS_KEY') {
            var f = new FormData(form), body = 'Name: ' + (f.get('name') || '') + '\nBusiness: ' + (f.get('business') || '') + '\nPhone: ' + (f.get('phone') || '') + '\nEmail: ' + (f.get('email') || '') + '\n\n' + (f.get('message') || '');
            location.href = 'mailto:info@seamlessflow.ai?subject=' + encodeURIComponent('New lead from seamlessflow.ai') + '&body=' + encodeURIComponent(body);
            return;
        }
        var btn = form.querySelector('button[type=submit]');
        btn.disabled = true; st.className = 'st'; st.textContent = 'Sending...';
        fetch(form.action, { method: 'POST', headers: { 'Accept': 'application/json' }, body: new FormData(form) })
        .then(function (r) { return r.json(); })
        .then(function (d) {
            if (!d.success) throw new Error(d.message || 'failed');
            form.reset(); st.className = 'st ok'; st.textContent = "Got it! We'll get back to you the same day.";
            if (typeof gtag !== 'undefined') gtag('event', 'generate_lead', { method: 'contact_form' });
        })
        .catch(function () { st.className = 'st bad'; st.innerHTML = 'Something went wrong. Please text or call <a href="tel:+13477498146">(347) 749-8146</a>.'; })
        .finally(function () { btn.disabled = false; });
    });

    // Phone taps are counted like the old site did.
    $$('a[href^="tel:"]').forEach(function (a) { a.addEventListener('click', function () { if (typeof gtag !== 'undefined') gtag('event', 'phone_click', { event_category: 'engagement', event_label: 'phone_number' }); }); });

    if ($('#sv')) (function () {
    // Stories: one per step. Auto-advance, tap right/left, hold to pause.
    var sv = $('#sv'), items = $$('#sr li'), bars = $('#sv-bars'), vid = $('#sv-vid'), cur = 0, down = 0;
    items.forEach(function () { bars.appendChild(document.createElement('i')).appendChild(document.createElement('b')); });
    function go(i) {
        if (i < 0) i = 0;
        if (i >= items.length) { sv.close(); return; }
        cur = i;
        var li = items[i], d = li.dataset, poster = A + 'feed/' + d.v + '.jpg';
        [].forEach.call(bars.children, function (bar, k) {
            bar.className = k < i ? 'done' : (k === i ? 'now' : '');
            if (k === i) { var nb = document.createElement('b'); bar.replaceChild(nb, bar.firstChild); nb.addEventListener('animationend', function () { go(cur + 1); }); }
        });
        vid.poster = poster;
        if (calm) vid.removeAttribute('src'); else { vid.src = A + 'feed/' + d.v + '.mp4'; var p = vid.play(); if (p) p.catch(function () {}); }
        $('#sv-bg').style.backgroundImage = 'url(' + poster + ')';
        $('#sv-week').textContent = '· ' + d.week;
        $('#sv-tag').textContent = 'Step ' + d.n + (d.once === '1' ? ' · once, at the start' : ' · every month');
        $('#sv-title').textContent = li.querySelector('h3').textContent;
        $('#sv-text').textContent = li.querySelector('p').textContent;
        li.classList.add('seen');
        sv.classList.remove('paused');
    }
    $$('[data-story]').forEach(function (b) { b.addEventListener('click', function () { go(+b.dataset.story); if (!sv.open) sv.showModal(); }); });
    [['#sv-prev', -1], ['#sv-next', 1]].forEach(function (z) {
        var el = $(z[0]);
        el.addEventListener('pointerdown', function () { down = Date.now(); sv.classList.add('paused'); vid.pause(); });
        el.addEventListener('pointerup', function () { var tap = Date.now() - down < 300; sv.classList.remove('paused'); if (tap) go(cur + z[1]); else if (!calm) vid.play(); });
        el.addEventListener('pointercancel', function () { sv.classList.remove('paused'); });
        el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(cur + z[1]); } });
    });
    sv.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') go(cur + 1); if (e.key === 'ArrowLeft') go(cur - 1); });
    $('#sv-close').addEventListener('click', function () { sv.close(); });
    sv.addEventListener('close', function () { vid.pause(); vid.removeAttribute('src'); vid.load(); [].forEach.call(bars.children, function (b) { b.className = ''; }); });
    $('#sr-next').addEventListener('click', function () { var r = $('#sr'); r.scrollBy({ left: 300 }); });
    if (location.hash === '#stories') { go(0); sv.showModal(); }
    })();
})();
