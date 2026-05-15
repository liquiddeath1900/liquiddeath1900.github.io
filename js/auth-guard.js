// seamlessflow.ai — Auth Guard
// Include in <head> of private pages AFTER supabase-config.js + supabase-auth.js.
// Requires: <style id="auth-hide">body{visibility:hidden}</style> in <head>.

const ALLOWED_EMAILS = [
  'seamlessflow.ai@gmail.com'
];

(async function authGuard() {
  const loginPage = 'login.html';

  try {
    let session = await getSession();

    if (!session || !session.user) {
      // Session may be refreshing — wait briefly for auth state change
      session = await new Promise((resolve) => {
        const sb = getSupabase();
        const timeout = setTimeout(() => resolve(null), 3000);
        sb.auth.onAuthStateChange((_event, s) => {
          clearTimeout(timeout);
          resolve(s);
        });
      });
    }

    if (!session || !session.user) {
      const currentPage = window.location.pathname.split('/').pop() || 'index.html';
      window.location.replace(loginPage + '?redirect=' + encodeURIComponent(currentPage));
      return;
    }

    const email = (session.user.email || '').toLowerCase();
    if (!ALLOWED_EMAILS.includes(email)) {
      await signOut();
      window.location.replace(loginPage + '?error=denied');
      return;
    }

    document.body.style.visibility = 'visible';
    const hideStyle = document.getElementById('auth-hide');
    if (hideStyle) hideStyle.remove();

    // Wire up any pre-rendered sign-out elements (class="auth-signout"), or fall back to a floating pill.
    const handleSignOut = async (e) => {
      if (e) e.preventDefault();
      await signOut();
      window.location.replace(loginPage);
    };
    const preRendered = document.querySelectorAll('.auth-signout');
    if (preRendered.length > 0) {
      preRendered.forEach(el => {
        el.classList.remove('hidden');
        el.setAttribute('aria-label', 'Sign out of ' + email);
        el.addEventListener('click', handleSignOut);
      });
    } else {
      // Fallback: floating button
      const btn = document.createElement('button');
      btn.id = 'auth-signout';
      btn.type = 'button';
      btn.textContent = 'Sign out';
      btn.setAttribute('aria-label', 'Sign out of ' + email);
      btn.style.cssText = 'position:fixed;top:calc(env(safe-area-inset-top) + 70px);right:14px;z-index:9999;padding:6px 12px;min-height:32px;background:rgba(0,0,0,.75);color:#fff;border:none;border-radius:999px;font:600 11px/1 -apple-system,system-ui,sans-serif;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.2)';
      btn.addEventListener('click', handleSignOut);
      document.body.appendChild(btn);
    }

  } catch (err) {
    console.error('Auth guard error:', err);
    window.location.replace(loginPage);
  }
})();
