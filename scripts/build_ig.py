"""Builds every public page in the social-feed look.

    python3 scripts/build_ig.py          -> writes preview/*.html  (noindex, no analytics; safe to look at)
    python3 scripts/build_ig.py --live   -> writes the real pages in the site root (SEO tags + analytics)

Shared pieces:  assets/css/ig.css, assets/js/ig.js
Page content:   this file, plus scripts/ig/*.html (homepage body, story viewer, icons, legal text).
The legal text in scripts/ig/ is the source for the three legal pages. Edit it there.
FAQ answers must match the terms of service.
"""
import json, os, re, sys, html

LIVE = "--live" in sys.argv
OUT = "" if LIVE else "preview/"
P = "" if LIVE else "../"            # path from a page back to the site root
HOME = "/" if LIVE else "index.html"
SITE = "https://www.seamlessflow.ai/"
GA = "G-B68C3RNBVD"
SMS = "sms:+13477498146?&body=Hi%20SeamlessFlow%21%20I%20found%20you%20on%20your%20website%20and%20want%20to%20talk%20about%20content%20for%20my%20business.%20My%20business%20is%3A%20"


def part(name):
    return open(f"scripts/ig/{name}").read()


def ver(path):
    return str(int(os.path.getmtime(path)))


def ic(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


AV = '<i class="av" aria-hidden="true">SF</i>'
ACTS = ('<div class="acts"><button type="button" class="like" aria-label="Like" aria-pressed="false">' + ic("heart") + '</button>'
        + ic("comment") + ic("send") + '{dots}' + ic("bookmark") + '</div>')


def post_head(sub):
    return f'<div class="post-head">{AV}<span class="who"><b>seamlessflow.ai</b><small>{sub}</small></span>{ic("dots")}</div>'


def acts(n=0):
    dots = '<span class="dots" aria-hidden="true"><i class="on"></i>' + "<i></i>" * (n - 1) + "</span>" if n else ""
    return ACTS.format(dots=dots)


def carousel(slides, label):
    n = len(slides)
    return (f'<div class="car-wrap"><div class="car" tabindex="0" aria-label="{label}">' + "".join(slides) + "</div>"
            f'<span class="count" aria-hidden="true">1/{n}</span>'
            f'<button class="car-btn prev" type="button" aria-label="Previous slide">{ic("left")}</button>'
            f'<button class="car-btn next" type="button" aria-label="Next slide">{ic("right")}</button></div>' + acts(n))


SWIPE = ('<span class="swipe" aria-hidden="true">Swipe <span class="arrows">' + ic("right") * 3 + "</span></span>")


def dm(title, text, tag="h2", cls=""):
    """The closing message thread. The message box is the Let's Talk button."""
    return f'''<div class="dm {cls}">
            <div class="dm-head"><i class="av lg" aria-hidden="true">SF</i><div><b>seamlessflow.ai</b><small>Replies the same day</small></div></div>
            <div class="dm-body">
                <div class="day" aria-hidden="true">Today</div>
                <div class="from">{AV}<div class="stack"><div class="bubble"><{tag}>{title}</{tag}></div><p class="bubble">{text}</p></div></div>
            </div>
            <a class="composer text-cta" href="{SMS}"><span aria-hidden="true">Message…</span><span class="send">Let's Talk{ic("send")}</span></a>
        </div>'''


# ---------------------------------------------------------------- shared chrome
def chrome(page, title):
    home = page == "index"
    a = (lambda x: "#" + x) if home else (lambda x: HOME + "#" + x)
    cur = lambda p: ' class="cur"' if p == page else ""
    how_rail = (f'<button type="button" data-story="0" aria-label="How it works">{ic("reels")}<span>How it works</span></button>' if home
                else f'<a href="{a("stories")}" aria-label="How it works">{ic("reels")}<span>How it works</span></a>')
    how_pill = (f'<button type="button" data-story="0" aria-label="How it works">{ic("reels")}</button>' if home
                else f'<a href="{a("stories")}" aria-label="How it works">{ic("reels")}</a>')
    talk = a("talk") if home else "book-call.html"
    rail = f'''<aside class="side">
    <a class="side-logo" href="{'#top' if home else HOME}" aria-label="SeamlessFlow home"><img class="wm" src="assets/img/wordmark.png" alt="SeamlessFlow.ai" width="565" height="66">{AV}</a>
    <nav aria-label="Main">
        <a href="{'#top' if home else HOME}"{cur("index")}>{ic("home")}<span>Home</span></a>
        <a href="faq.html"{cur("faq")} aria-label="FAQ">{ic("search")}<span>FAQ</span></a>
        {how_rail}
        <a href="industries.html"{cur("industries")} aria-label="Industries">{ic("compass")}<span>Industries</span></a>
        <a href="{talk}"{cur("book-call")} aria-label="Messages">{ic("send")}<span>Messages</span></a>
        <a href="{a("packages")}" aria-label="Packages">{ic("plus")}<span>Packages</span></a>
        <a href="about.html"{cur("about")} aria-label="About">{AV}<span>About</span></a>
        <button class="more" type="button" data-menu aria-label="More">{ic("menu")}<span>More</span></button>
    </nav>
</aside>'''
    if home:
        bar = f'''<header class="fbar">
    <button type="button" data-menu aria-label="Menu">{ic("plus")}</button>
    <a href="#top" class="wm-link" aria-label="SeamlessFlow home"><img class="wm" src="assets/img/wordmark.png" alt="SeamlessFlow.ai" width="565" height="66"></a>
    <a href="#packages" aria-label="Packages">{ic("heart")}</a>
</header>'''
    else:
        bar = f'''<header class="fbar">
    <a href="{HOME}" aria-label="Back to home">{ic("left")}</a>
    <b>{title}</b>
    <button type="button" data-menu aria-label="Menu">{ic("menu")}</button>
</header>'''
    pill = f'''<nav class="pill" aria-label="Quick links">
    <a href="{'#top' if home else HOME}"{cur("index")} aria-label="Home">{ic("home")}</a>
    {how_pill}
    <a href="{talk}"{cur("book-call")} aria-label="Messages">{ic("send")}</a>
    <a href="faq.html"{cur("faq")} aria-label="FAQ">{ic("search")}</a>
    <a href="about.html"{cur("about")} aria-label="About">{AV}</a>
</nav>'''
    menu = f'''<dialog class="sheet" id="menu" aria-label="Menu">
    <a href="{HOME}">Home</a>
    <a href="about.html">About</a>
    <a href="industries.html">Industries</a>
    <a href="faq.html">FAQ</a>
    <a href="book-call.html">Contact us</a>
    <a href="https://seamlessflow-hub.vercel.app/login">Client Login</a>
    <button type="button" data-close>Cancel</button>
</dialog>'''
    footer = f'''<footer>
    <ul>
        <li><a href="about.html">About</a></li>
        <li><a href="industries.html">Industries</a></li>
        <li><a href="{a("packages")}">Packages</a></li>
        <li><a href="faq.html">FAQ</a></li>
        <li><a href="book-call.html">Contact us</a></li>
        <li><a href="https://seamlessflow-hub.vercel.app/login">Client Login</a></li>
        <li><a href="privacy-policy.html">Privacy</a></li>
        <li><a href="terms-of-service.html">Terms</a></li>
        <li><a href="cookies-policy.html">Cookies</a></li>
    </ul>
    <ul>
        <li><a href="tel:+13477498146">(347) 749-8146</a></li>
        <li><a href="mailto:info@seamlessflow.ai">info@seamlessflow.ai</a></li>
        <li><a href="https://instagram.com/seamlessflow.ai" target="_blank" rel="noopener noreferrer">Instagram</a></li>
        <li><a href="https://www.youtube.com/@SeamlessflowSEO" target="_blank" rel="noopener noreferrer">YouTube</a></li>
        <li><a href="https://linkedin.com/company/seamlessflow" target="_blank" rel="noopener noreferrer">LinkedIn</a></li>
        <li><a href="https://x.com/seamlessflowai" target="_blank" rel="noopener noreferrer">X</a></li>
    </ul>
    <p>&copy; 2026 SeamlessFlow.ai · NYC based, available to travel</p>
</footer>'''
    return rail, bar, pill, menu, footer


def head(page, title, desc, og_desc=None, schema=None, og_title=None):
    url = SITE if page == "index" else f"{SITE}{page}.html"
    t, d = html.escape(title, quote=True), html.escape(desc, quote=True)
    og = html.escape(og_desc or desc, quote=True)
    ogt = html.escape(og_title or title, quote=True)
    robots = "" if LIVE else '    <meta name="robots" content="noindex, nofollow">\n'
    fav = "/" if LIVE else P
    extra = ""
    if LIVE and page == "index":
        extra += "    <script>if (location.pathname === '/index.html') location.replace(location.origin + '/');</script>\n"
    for sc in schema or []:
        extra += '    <script type="application/ld+json">' + sc + "</script>\n"
    return f'''<!DOCTYPE html>
<html lang="en" data-a="{P}assets/">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
{robots}    <title>{t}</title>
    <meta name="description" content="{d}">
    <link rel="canonical" href="{url}">
    <link rel="icon" type="image/x-icon" href="{fav}favicon.ico">
    <link rel="icon" type="image/svg+xml" href="{fav}favicon.svg">
    <link rel="icon" type="image/png" sizes="96x96" href="{fav}favicon-96x96.png">
    <link rel="apple-touch-icon" sizes="180x180" href="{fav}apple-touch-icon.png">
    <link rel="manifest" href="{fav}site.webmanifest">
    <meta name="theme-color" content="#ffffff">
    <meta name="apple-mobile-web-app-title" content="SeamlessFlow">
    <meta property="og:title" content="{ogt}">
    <meta property="og:description" content="{og}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:site_name" content="SeamlessFlow">
    <meta property="og:image" content="{SITE}assets/og-seamlessflow-2026.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="SeamlessFlow: Content that makes a difference. Customers that keep coming.">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{ogt}">
    <meta name="twitter:description" content="{og}">
    <meta name="twitter:image" content="{SITE}assets/og-seamlessflow-2026.jpg">
{extra}    <link rel="stylesheet" href="{P}assets/css/ig.css?v={ver("assets/css/ig.css")}">
</head>
'''


def build(page, title, desc, main, bar_title="", og_desc=None, schema=None, dialogs="", og_title=None):
    rail, bar, pill, menu, footer = chrome(page, bar_title)
    ga = f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>window.dataLayer = window.dataLayer || []; function gtag(){{dataLayer.push(arguments);}} gtag('js', new Date()); gtag('config', '{GA}');</script>
''' if LIVE else ""
    doc = (head(page, title, desc, og_desc, schema, og_title) + f'<body id="top">\n\n{part("sprite.html")}\n\n{rail}\n\n<div class="wrap">\n{bar}\n\n'
           + main + f"\n\n{footer}\n</div>\n\n{pill}\n\n{dialogs}{menu}\n\n"
           + f'<script src="{P}assets/js/ig.js?v={ver("assets/js/ig.js")}"></script>\n{ga}</body>\n</html>\n')
    if P:  # preview pages live one folder down, so asset paths step back up
        doc = doc.replace('"assets/', f'"{P}assets/').replace("(assets/", f"({P}assets/")
    open(f"{OUT}{page}.html", "w").write(doc)
    print("built", f"{OUT}{page}.html", f"{len(doc) // 1024}KB")


# ---------------------------------------------------------------- home
home_main = part("home_main.html")
build("index", "Done-For-You Content & Ads Agency NYC | SeamlessFlow",
      "Done-for-you content and ads agency in NYC. We plan, script, film, edit, post, and run ads on the videos that work. Text us to get started.",
      home_main, og_title="SeamlessFlow | Content that makes a difference",
      og_desc="Content that makes a difference. Brand growth is what we do best.",
      schema=[part("schema_home.json").strip()], dialogs=part("story_dialog.html") + "\n\n")

# ---------------------------------------------------------------- about (the profile)
values = [
    ("Show the real thing", "Real people, real work, real results. Your customers can tell when it's staged."),
    ("Numbers over guesses", "Every month is planned off what the last one taught us, not what's trending."),
    ("Move fast", "The sooner your content is live, the sooner we know what works and can put money behind it."),
    ("Partners, not vendors", "We win when you win. That's why we start by understanding your goals, not selling you a package."),
]
goals = [
    "Help every client become the name people think of first in their area",
    "Turn content into a steady flow of customers, not just views",
    "Build long-term partnerships where results grow every month",
    "Grow a team of creators and editors who care about the work as much as we do",
]
believe = carousel(
    [f'<div class="slide cover img"><video class="tm feed-vid" muted loop playsinline preload="none" poster="assets/feed/b-cover.jpg" data-src="assets/feed/b-cover.mp4" aria-hidden="true"></video><h2>What we believe</h2>{SWIPE}</div>']
    + [f'<div class="slide img"><video class="tm feed-vid" muted loop playsinline preload="none" poster="assets/feed/{v}.jpg" data-src="assets/feed/{v}.mp4" aria-hidden="true"></video>'
       f'<span class="n">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></div>' for i, ((t, d), v) in enumerate(zip(values, ("b-real", "b-numbers", "b-fast", "b-partners")))],
    "What we believe, 5 slides")
about_main = f'''<main>
    <div class="col">
        <section class="ph about-head" aria-label="SeamlessFlow">
            <a class="ph-av" href="{HOME}#stories" aria-label="Watch how it works"><span aria-hidden="true">SF</span></a>
            <div class="ph-handle">seamlessflow.ai</div>
            <ul class="ph-stats">
                <li><b>10+</b> years in social media</li>
                <li><b>NYC</b> based, and we travel</li>
                <li><b>5</b> platforms</li>
            </ul>
            <div class="ph-bio">
                <div class="ph-name">SeamlessFlow</div>
                <div class="ph-cat">Brand growth agency</div>
                <h1>Over 10 years of social media experience. Now we're putting it to work for you.</h1>
                <p>SeamlessFlow is a brand growth agency based in New York City. We make content that shows the world how good you are, and we take care of bringing in your customers for years to come.</p>
                <ul class="ph-lines">
                    <li>{ic("mappin")}New York City</li>
                    <li>{ic("reels")}Instagram, Facebook, TikTok, YouTube, Google</li>
                </ul>
            </div>
            <div class="ph-btns">
                <a class="btn blue text-cta" href="{SMS}">Let's Talk</a>
                <a class="btn" href="{HOME}#packages">See Packages</a>
            </div>
        </section>
    </div>
    <div class="shell one">
        <div class="feed">
            <article class="post" id="founder">
                {post_head("The founder")}
                <div class="media plain"><img class="tm" src="assets/img/founder-victorious-mota.jpg" alt="Victorious Mota, founder of SeamlessFlow" width="579" height="724" decoding="async"></div>
                {acts()}
                <div class="post-cap"><h2 class="cap-h">Victorious Mota</h2>
                    <p>I've spent over 10 years in social media, learning what makes people stop scrolling and actually pay attention.</p>
                    <p>Along the way I learned that great businesses don't lose to better businesses. They lose to the ones people have heard of. So I built SeamlessFlow to fix that: a team that handles the whole process, from the plan to the post to the ads, so owners can focus on doing great work.</p>
                    <p>Every client gets the same thing I'd want for my own brand: a clear plan, content that feels real, and honest numbers every month.</p>
                </div>
            </article>
            <article class="post" id="believe">
                {post_head("What we believe")}
                {believe}
            </article>
            <article class="post" id="going">
                {post_head("Where we're going")}
                <div class="post-card"><h2>Where we're going</h2></div>
                {acts()}
                <div class="post-cap"><b>seamlessflow.ai</b> We're building the agency we'd want to hire: fast, honest, and focused on what actually grows a business.
                    <ul class="checks">{"".join(f"<li>{ic('check')}<span>{g}</span></li>" for g in goals)}</ul>
                </div>
            </article>
        </div>
        <section id="talk" class="talk">
        {dm("Let's build your brand.", "Text us what you do. We'll get back to you the same day, audit where you stand, and show you the plan.")}
        </section>
    </div>
</main>'''
build("about", "About SeamlessFlow | Brand Growth Agency in NYC",
      "Over 10 years of social media experience. SeamlessFlow is a NYC brand growth agency that plans, films, posts, and runs ads to bring in customers.",
      about_main, bar_title="seamlessflow.ai")

# ---------------------------------------------------------------- industries (explore grid + a post each)
INDUSTRIES = [
    ("roofing", "Roofing", "Roofer carrying materials across a roof",
     "Homeowners hand over thousands for a roof they can't see. Video lets them see your crew, your work, and your standards before they ever call.",
     ["Tear-off to finish time-lapses", "Storm damage walk-throughs", "Crew and owner on camera"]),
    ("hvac", "HVAC", "Technician checking gauges on an air conditioning unit",
     "Nobody thinks about HVAC until it breaks. Staying in front of people all year means you're the name they remember when it does.",
     ["Seasonal maintenance tips", "Install day from start to finish", "Answers to the questions customers always ask"]),
    ("plumbing", "Plumbing", "Plumber holding a pipe wrench",
     "People let you into their homes in an emergency. Content builds the trust before the emergency happens.",
     ["Before and after fixes", "\"Don't do this\" tips that save customers money", "Meet the plumber who's coming to your house"]),
    ("electrical", "Electrical", "Electrician working on a control panel",
     "Electrical work is invisible once the walls close. Showing it is how you prove the quality people are paying for.",
     ["Panel upgrades explained simply", "Safety red flags in older homes", "Clean installs people want to show off"]),
    ("remodeling", "Remodeling + Contractors", "Contractor hammering a nail into a wall",
     "Remodels are big decisions. Video shows the craftsmanship and the process so clients pick you with confidence.",
     ["Full transformation reveals", "Day-in-the-life on a job site", "Client walk-throughs at handover"]),
    ("junk-removal", "Junk Removal", "Two crew members loading a van",
     "Junk removal is made for short video. Big loads, fast crews, and clean spaces stop people mid-scroll.",
     ["Full clean-outs in under a minute", "\"Guess the weight\" style hooks", "What happens to the stuff after pickup"]),
    ("moving", "Moving", "Mover taping up boxes",
     "Moving is stressful. Showing a careful, friendly crew is what makes people trust you with everything they own.",
     ["How your crew packs and protects", "Moving day start to finish", "Tips that make moving day easier"]),
    ("landscaping", "Landscaping", "Landscaper trimming a tall hedge",
     "Outdoor work is some of the most satisfying content there is. A great before and after sells the next job.",
     ["Yard transformations", "Seasonal care tips", "Design walk-throughs with the owner"]),
]
tiles = "".join(f'<a href="#{s}"><img src="assets/ind/{s}.jpg" alt="" width="800" height="1000" loading="lazy" decoding="async"><span>{n}</span></a>'
                for s, n, alt, why, ideas in INDUSTRIES)
ind_posts = "".join(f'''
            <article class="post" id="{s}">
                {post_head(n)}
                <div class="media named"><img class="tm" src="assets/ind/{s}.jpg" alt="{alt}" width="800" height="1000" loading="lazy" decoding="async"><div class="ov"><h2>{n}</h2></div></div>
                {acts()}
                <div class="post-cap"><b>seamlessflow.ai</b> {why}
                    <span class="lbl">Content we'd make</span>
                    <ul class="vlist">{"".join(f"<li>{ic('video')}<span>{x}</span></li>" for x in ideas)}</ul>
                </div>
            </article>''' for s, n, alt, why, ideas in INDUSTRIES)
industries_main = f'''<main>
    <div class="col">
        <header class="page-cap">
            <h1>Built for service businesses that do great work</h1>
            <p>When one job is worth thousands, being the name people trust matters. Here's who we work with most, and the kind of content that works for them.</p>
        </header>
        <nav class="xgrid" aria-label="Industries">{tiles}<a class="other" href="#other"><span>Don't see your industry?</span></a></nav>
    </div>
    <div class="shell one">
        <div class="feed" style="padding-top:18px">{ind_posts}
            <article class="post" id="other">
                {post_head("Everyone else")}
                <div class="post-card"><h2>Don't see your industry?</h2></div>
                {acts()}
                <p class="post-cap"><b>seamlessflow.ai</b> We work with any business that's serious about growing. If people buy from you, we can make content that brings them in.</p>
            </article>
        </div>
        <section id="talk" class="talk">
        {dm("Ready to be the name people call?", "Text us what you do. We'll get back to you the same day and show you what content can do for your business.")}
        </section>
    </div>
</main>'''
build("industries", "Industries We Work With | SeamlessFlow",
      "Content and ads for roofing, HVAC, plumbing, electrical, remodeling, junk removal, moving, and landscaping companies.",
      industries_main, bar_title="Industries")

# ---------------------------------------------------------------- faq (search + comment threads)
PK = f'<a href="{HOME}#packages">See what\'s in each package</a>'
GROUPS = [
 ("Getting started", [
  ("How do we get started?",
   "Text or call us. We set up a discovery call, learn about your business and goals, then audit your Google profile and social accounts to see where you stand. You get a quote with the right package. Once you approve it, we start onboarding."),
  ("How fast can we get going?",
   "It depends on your package and what the audit finds. You can see results in as little as 30, 15, or 7 days depending on the package. By results we mean your first videos live and real numbers coming in."),
  ("Do I have to be on camera?",
   "No, but it helps. People buy from people, and owners on camera usually perform best. If that's not you, your team can be the face, or we build content around the work itself. Either way, we write what to say and coach you through it."),
  ("How much of my time does this take?",
   "Not much. On shoot day we come to you and film at your shop, office, or job site. The scripts are a guide, not lines to memorize. You say it your way, in your own words and your own rhythm. Between shoots, film a few stories from the shot list we send and review content when it's ready. We handle the planning, editing, posting, and ads."),
 ]),
 ("Pricing and contracts", [
  ("How much does it cost?",
   "Packages start at $3,000, $4,500, and $8,000 a month. Your final price is set after your audit, based on your market, locations, and shoot volume. There's also a one-time onboarding fee set by what the audit finds. Ad spend is separate and paid directly to the platforms. Accounts that are already in good shape cost less to start. " + PK + "."),
  ("Is there a contract?",
   "Launch and Growth have a 3-month minimum. Full Service has 6 months. Content builds on itself, and the first months are when we learn what your audience responds to. After the minimum, it's month to month with 30 days' notice."),
  ("Is ad spend included?",
   "No. You pay the ad platforms directly with your own card, so you always see exactly where your money goes. We never mark up your ad spend."),
  ("Do you travel?",
   "Yes. We're based in New York City and travel for clients. Shoots outside the area include a travel fee, quoted up front."),
 ]),
 ("The content", [
  ("What platforms do you cover?",
   "Instagram, Facebook, TikTok, and YouTube on every package. Full Service also covers Google SEO and your Google Business Profile."),
  ("Do I approve content before it goes live?",
   "Yes. We send everything for review first. You have 2 business days to approve or ask for changes, so your schedule never stalls."),
  ("How many revisions do I get?",
   "One round per video is included. Most changes are small because the scripts are approved before we film."),
  ("Who posts, and do you need my password?",
   "We post for you. Where the platform allows it, we ask to be added as a partner or manager instead of using your password. You always stay the owner of your accounts."),
  ("Will you reply to comments and DMs for me?",
   "On Growth and Full Service, yes. During onboarding we build a reply guide with you: approved answers to the questions you get most. We handle those replies, and Full Service adds auto-replies where the platform allows it. Anything that needs your expertise, like quotes or technical questions, gets sent straight to you so no lead slips through. You're the expert, so you always get the final word."),
  ("Do I own the content?",
   "Yes. Once paid, the final videos are yours to use for your business. Raw footage is available on request for a fee."),
 ]),
 ("Results", [
  ("How long until I see real results?",
   "First videos and numbers come fast. Steady leads usually build over the first 3 to 6 months as we learn what works and put ad money behind it. Every month gets sharper than the last."),
  ("Do you guarantee results?",
   "No honest agency can guarantee views, followers, or sales. Platforms change, and results depend on your market and how you treat your customers. What we guarantee is the work: a clear plan, content on schedule, and honest numbers every month."),
  ("How do you report results?",
   "On the discovery call we agree on the number that matters to you, like calls, bookings, or sales. Reports track that, not just likes. Launch gets a monthly report, Growth every two weeks, and Full Service weekly with a strategy call."),
  ("Do I need ads, or is organic enough?",
   "Both work better together. Organic posts show us which videos people actually like. Ads take those winners and put them in front of more of the right people, faster."),
  ("What if I'm not happy?",
   "Tell us. We'll look at what's not working and change it in the next month's plan. After your minimum term, you can cancel any time with 30 days' notice."),
 ]),
]
faq_schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
    for _, qs in GROUPS for q, a in qs]})
chips = '<button type="button" class="on" data-g="all" aria-pressed="true">All</button>' + "".join(
    f'<button type="button" data-g="{i}" aria-pressed="false">{g}</button>' for i, (g, _) in enumerate(GROUPS))
threads = "".join(f'''
        <section class="faq-g" data-g="{i}">
            <h2>{g}</h2>
            <ul class="cm faq">{"".join(f"""
                <li><details>
                    <summary><i class="av yb" aria-hidden="true">YB</i><div><h3>{q}</h3><div class="meta"><span class="v">View reply</span><span class="h">Hide reply</span></div></div></summary>
                    <div class="re">{AV}<p><b>seamlessflow.ai</b><span class="tag">Author</span> {a}</p></div>
                </details></li>""" for q, a in qs)}
            </ul>
        </section>''' for i, (g, qs) in enumerate(GROUPS))
faq_main = f'''<main class="shell one wide">
        <header class="page-cap">
            <h1>Questions, answered</h1>
            <p>The things business owners ask us most. Don't see yours? Text us.</p>
        </header>
        <label class="search">{ic("search")}<input type="search" id="faq-q" placeholder="Search questions" aria-label="Search questions" autocomplete="off"></label>
        <div class="chips" aria-label="Topics">{chips}</div>
{threads}
        <p class="faq-none" hidden>Nothing matches that. Text us and we'll answer it.</p>
        <section id="talk" class="talk" style="padding-top:26px">
        {dm("Still have questions?", "Send us a text and we'll get back to you the same day.", cls="full")}
        </section>
</main>'''
build("faq", "FAQ | SeamlessFlow",
      "Answers to common questions about our content and ads packages: pricing, contracts, ad spend, approvals, ownership, and results.",
      faq_main, bar_title="FAQ", schema=[faq_schema])

# ---------------------------------------------------------------- contact (a message thread)
contact_main = f'''<main class="shell one wide">
    <div class="dm full" id="contact">
        <div class="dm-head"><i class="av lg" aria-hidden="true">SF</i><div><b>seamlessflow.ai</b><small>Replies the same day</small></div></div>
        <div class="dm-body">
            <div class="day" aria-hidden="true">Today</div>
            <div class="from">{AV}<div class="stack">
                <div class="bubble"><h1 class="h2" style="font-size:clamp(20px,5.4vw,24px)">Fastest way to reach us</h1></div>
                <p class="bubble">Text or call. We get back to you the same day.</p>
                <p class="bubble"><a class="big-tel" href="tel:+13477498146">(347) 749-8146</a></p>
            </div></div>
        </div>
        <div class="quick">
            <a class="fill text-cta" href="{SMS}">{ic("comment")}Text Us</a>
            <a href="tel:+13477498146">{ic("phone")}Call Us</a>
        </div>
        <div class="dm-body" id="email" style="padding-top:6px">
            <div class="from">{AV}<div class="stack">
                <div class="bubble"><h2>Rather write it out?</h2></div>
                <p class="bubble">Send us a message and it lands straight in our inbox. Or email <a class="ln" href="mailto:info@seamlessflow.ai">info@seamlessflow.ai</a>.</p>
            </div></div>
        </div>
        <form id="contact-form" class="cform" action="https://api.web3forms.com/submit" method="POST">
            <input type="hidden" name="access_key" value="WEB3FORMS_ACCESS_KEY">
            <input type="hidden" name="subject" value="New lead from seamlessflow.ai">
            <input type="hidden" name="from_name" value="SeamlessFlow website">
            <input type="checkbox" name="botcheck" hidden tabindex="-1" autocomplete="off">
            <div><label for="cf-name">Your name *</label><input id="cf-name" name="name" type="text" required autocomplete="name"></div>
            <div><label for="cf-business">Business name and what you do *</label><input id="cf-business" name="business" type="text" required autocomplete="organization"></div>
            <div class="two">
                <div><label for="cf-phone">Phone *</label><input id="cf-phone" name="phone" type="tel" required autocomplete="tel"></div>
                <div><label for="cf-email">Email</label><input id="cf-email" name="email" type="email" autocomplete="email"></div>
            </div>
            <div><label for="cf-message">What do you want help with?</label><textarea id="cf-message" name="message" rows="4"></textarea></div>
            <button type="submit">Send message{ic("send")}</button>
            <p id="cf-status" class="st" role="status" aria-live="polite"></p>
        </form>
    </div>
</main>'''
build("book-call", "Contact Us | SeamlessFlow",
      "Text, call, or message SeamlessFlow. We get back to you the same day and tell you which content package fits your business.",
      contact_main, bar_title="Messages", og_desc="You talk on camera. We plan, film, edit, post, and run ads on what works.")

# ---------------------------------------------------------------- legal (plain documents)
for slug, title, desc, bar in [
    ("terms-of-service", "Terms of Service | SeamlessFlow", "The terms for working with SeamlessFlow: packages, onboarding, billing, shoot days, approvals, content ownership, and more.", "Terms"),
    ("privacy-policy", "Privacy Policy | SeamlessFlow", "How SeamlessFlow collects, uses, and protects your information.", "Privacy"),
    ("cookies-policy", "Cookies Policy | SeamlessFlow", "The cookies and similar tools seamlessflow.ai uses and how to control them.", "Cookies"),
]:
    build(slug, title, desc, f'<main class="shell one doc">\n{part(slug + ".html")}</main>', bar_title=bar)
