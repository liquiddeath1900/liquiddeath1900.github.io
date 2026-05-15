// seamlessflow.ai — Supabase Auth helpers (slim)
// Requires supabase-config.js loaded first and the supabase-js v2 CDN script.

let _sb = null;

function getSupabase() {
  if (_sb) return _sb;
  if (typeof supabase === 'undefined') return null;
  _sb = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  return _sb;
}

async function getUser() {
  const sb = getSupabase();
  if (!sb) return null;
  const { data } = await sb.auth.getUser();
  return data?.user || null;
}

async function getSession() {
  const sb = getSupabase();
  if (!sb) return null;
  const { data } = await sb.auth.getSession();
  return data?.session || null;
}

async function signInWithEmail(email) {
  const sb = getSupabase();
  if (!sb) return { error: { message: 'Supabase not loaded' } };
  const { data, error } = await sb.auth.signInWithOtp({
    email,
    options: {
      shouldCreateUser: true,
      emailRedirectTo: window.location.origin + '/login.html'
    }
  });
  return { data, error };
}

async function signInWithGoogle() {
  const sb = getSupabase();
  if (!sb) return { error: { message: 'Supabase not loaded' } };
  const { data, error } = await sb.auth.signInWithOAuth({
    provider: 'google',
    options: { redirectTo: window.location.origin + '/login.html' }
  });
  return { data, error };
}

async function signOut() {
  const sb = getSupabase();
  if (!sb) return;
  await sb.auth.signOut();
}

function onAuthChange(callback) {
  const sb = getSupabase();
  if (!sb) return;
  sb.auth.onAuthStateChange((_event, session) => callback(session));
}
