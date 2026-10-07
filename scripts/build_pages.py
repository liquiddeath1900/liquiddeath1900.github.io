"""Builds industries.html and about.html on the book-call.html shell. Run site_chrome.py after."""
import re
from site_chrome import INDUSTRIES

BOOK = "book-call.html"
shell = open("book-call.html").read()
head = shell[:shell.index("<!-- NAV:START -->")]
tail = shell[shell.index("<!-- FOOTER:START -->"):]


def page(fname, title, desc, main):
    h = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', h)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', h)
    h = h.replace("https://www.seamlessflow.ai/book-call", "https://www.seamlessflow.ai/" + fname[:-5])
    open(fname, "w").write(h + "<!-- NAV:START -->\n<!-- NAV:END -->\n\n" + main + "\n" + tail)
    print("built", fname)


CTA = f'''    <section class="py-20 bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white">
        <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 class="text-3xl sm:text-4xl font-extrabold mb-4">{{h}}</h2>
            <p class="text-lg text-gray-300 mb-8">{{p}}</p>
            <a href="{BOOK}" class="btn-primary btn-shimmer text-white px-8 py-4 rounded-xl text-lg font-bold inline-flex items-center justify-center"><i class="fas fa-calendar-check mr-3"></i>Book a Discovery Call</a>
        </div>
    </section>
'''

# ---------- Industries ----------
# (slug, icon, name) come from site_chrome.INDUSTRIES so nav and page never drift.
COPY = {
    "roofing": ("Homeowners hand over thousands for a roof they can't see. Video lets them see your crew, your work, and your standards before they ever call.",
                ["Tear-off to finish time-lapses", "Storm damage walk-throughs", "Crew and owner on camera"]),
    "hvac": ("Nobody thinks about HVAC until it breaks. Staying in front of people all year means you're the name they remember when it does.",
             ["Seasonal maintenance tips", "Install day from start to finish", "Answers to the questions customers always ask"]),
    "plumbing": ("People let you into their homes in an emergency. Content builds the trust before the emergency happens.",
                 ["Before and after fixes", "\"Don't do this\" tips that save customers money", "Meet the plumber who's coming to your house"]),
    "electrical": ("Electrical work is invisible once the walls close. Showing it is how you prove the quality people are paying for.",
                   ["Panel upgrades explained simply", "Safety red flags in older homes", "Clean installs people want to show off"]),
    "remodeling": ("Remodels are big decisions. Video shows the craftsmanship and the process so clients pick you with confidence.",
                   ["Full transformation reveals", "Day-in-the-life on a job site", "Client walk-throughs at handover"]),
    "junk-removal": ("Junk removal is made for short video. Big loads, fast crews, and clean spaces stop people mid-scroll.",
                     ["Full clean-outs in under a minute", "\"Guess the weight\" style hooks", "What happens to the stuff after pickup"]),
    "moving": ("Moving is stressful. Showing a careful, friendly crew is what makes people trust you with everything they own.",
               ["How your crew packs and protects", "Moving day start to finish", "Tips that make moving day easier"]),
    "landscaping": ("Outdoor work is some of the most satisfying content there is. A great before and after sells the next job.",
                    ["Yard transformations", "Seasonal care tips", "Design walk-throughs with the owner"]),
}

cards = ""
for slug, icon, name in INDUSTRIES:
    why, ideas = COPY[slug]
    li = "".join(f'<li class="flex gap-2"><i class="fas fa-video text-blue-500 mt-1 text-xs"></i><span>{x}</span></li>' for x in ideas)
    cards += f'''
                <div id="{slug}" class="reveal bg-white rounded-2xl p-7 border border-gray-100 shadow-sm scroll-mt-24">
                    <div class="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center mb-4"><i class="fas {icon} text-xl"></i></div>
                    <h2 class="text-xl font-bold text-gray-900 mb-2">{name}</h2>
                    <p class="text-gray-600 mb-4">{why}</p>
                    <p class="text-xs font-bold uppercase tracking-wider text-gray-400 mb-2">Content we'd make</p>
                    <ul class="space-y-1.5 text-sm text-gray-700">{li}</ul>
                </div>'''

industries_main = f'''    <main id="home">
        <section class="pt-32 pb-16 bg-gray-950 text-white">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                <span class="text-blue-400 font-semibold uppercase tracking-wider text-sm">Industries</span>
                <h1 class="text-4xl sm:text-5xl font-extrabold mt-3 mb-5">Built for service businesses that do great work</h1>
                <p class="text-lg text-gray-300 max-w-2xl mx-auto">When one job is worth thousands, being the name people trust matters. Here's who we work with most, and the kind of content that works for them.</p>
            </div>
        </section>
        <section class="section-padding bg-gray-50">
            <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">{cards}
                </div>
                <div class="reveal mt-10 text-center bg-white rounded-2xl border-2 border-dashed border-blue-200 p-8">
                    <h2 class="text-2xl font-bold text-gray-900 mb-2">Don't see your industry?</h2>
                    <p class="text-gray-600 mb-6 max-w-xl mx-auto">We work with any business that's serious about growing. If people buy from you, we can make content that brings them in.</p>
                    <a href="{BOOK}" class="inline-flex items-center bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-bold"><i class="fas fa-calendar-check mr-2"></i>Let's talk about your business</a>
                </div>
            </div>
        </section>
''' + CTA.replace("{h}", "Ready to be the name people call?").replace("{p}", "30 minutes. We audit where you stand and show you what content can do for your business.") + "    </main>\n"

page("industries.html", "Industries We Work With | SeamlessFlow",
     "Content and ads for roofing, HVAC, plumbing, electrical, remodeling, junk removal, moving, and landscaping companies.",
     industries_main)

# ---------- About ----------
values = [
    ("fa-eye", "Show the real thing", "Real people, real work, real results. Your customers can tell when it's staged."),
    ("fa-chart-line", "Numbers over guesses", "Every month is planned off what the last one taught us, not what's trending."),
    ("fa-bolt", "Move fast", "The sooner your content is live, the sooner we know what works and can put money behind it."),
    ("fa-handshake", "Partners, not vendors", "We win when you win. That's why we start by understanding your goals, not selling you a package."),
]
vals = "".join(f'''
                    <div class="reveal bg-white rounded-2xl p-6 border border-gray-100 shadow-sm">
                        <i class="fas {i} text-blue-600 text-xl mb-3"></i>
                        <h3 class="font-bold text-gray-900 mb-1">{t}</h3>
                        <p class="text-gray-600 text-sm">{d}</p>
                    </div>''' for i, t, d in values)

goals = [
    "Help every client become the name people think of first in their area",
    "Turn content into a steady flow of customers, not just views",
    "Build long-term partnerships where results grow every month",
    "Grow a team of creators and editors who care about the work as much as we do",
]
goal_li = "".join(f'<li class="flex gap-3"><i class="fas fa-check-circle text-blue-400 mt-1"></i><span>{g}</span></li>' for g in goals)

about_main = f'''    <main id="home">
        <section class="pt-32 pb-20 bg-gray-950 text-white">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                <span class="text-blue-400 font-semibold uppercase tracking-wider text-sm">About us</span>
                <h1 class="text-4xl sm:text-5xl font-extrabold mt-3 mb-5">Over 10 years behind the camera.<br class="hidden sm:block"> Now we're putting it to work for you.</h1>
                <p class="text-lg text-gray-300 max-w-2xl mx-auto">SeamlessFlow is a brand growth agency based in New York City. We make content that shows the world how good you are, and we keep making it until the customers come.</p>
            </div>
        </section>

        <section class="section-padding bg-white">
            <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-5 gap-10 items-center">
                <div class="md:col-span-2 reveal">
                    <!-- TODO: replace with founder photo -->
                    <div class="aspect-[4/5] rounded-3xl bg-gradient-to-br from-blue-600 to-sky-400 flex items-center justify-center text-white text-6xl font-extrabold shadow-xl">VM</div>
                </div>
                <div class="md:col-span-3 reveal">
                    <span class="text-blue-600 font-semibold uppercase tracking-wider text-sm">The founder</span>
                    <h2 class="text-3xl font-extrabold text-gray-900 mt-2 mb-4">Victorious Mota</h2>
                    <p class="text-gray-700 leading-relaxed mb-4">I've been making content for over 10 years. Planning it, filming it, editing it, and figuring out what makes people stop scrolling and actually pay attention.</p>
                    <p class="text-gray-700 leading-relaxed mb-4">Along the way I learned that great businesses don't lose to better businesses. They lose to the ones people have heard of. So I built SeamlessFlow to fix that: a team that handles the whole process, from the plan to the post to the ads, so owners can focus on doing great work.</p>
                    <p class="text-gray-700 leading-relaxed">Every client gets the same thing I'd want for my own brand: a clear plan, content that feels real, and honest numbers every month.</p>
                </div>
            </div>
        </section>

        <section class="section-padding bg-gray-50">
            <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="text-center mb-10 reveal">
                    <h2 class="section-title font-extrabold text-gray-900 mb-3">What we believe</h2>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">{vals}
                </div>
            </div>
        </section>

        <section class="section-padding bg-gray-900 text-white">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
                <div class="reveal">
                    <h2 class="text-3xl sm:text-4xl font-extrabold mb-4">Where we're going</h2>
                    <p class="text-gray-300">We're building the agency we'd want to hire: fast, honest, and focused on what actually grows a business.</p>
                </div>
                <ul class="reveal space-y-4 text-gray-200">{goal_li}</ul>
            </div>
        </section>

        <section class="section-padding bg-white">
            <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
                <div class="reveal"><div class="text-5xl font-extrabold text-blue-600">10+</div><p class="text-gray-600 mt-2">Years making content</p></div>
                <div class="reveal"><div class="text-5xl font-extrabold text-blue-600">NYC</div><p class="text-gray-600 mt-2">Based, and we travel</p></div>
                <div class="reveal"><div class="text-5xl font-extrabold text-blue-600">5</div><p class="text-gray-600 mt-2">Platforms: Instagram, Facebook, TikTok, YouTube, Google</p></div>
            </div>
        </section>
''' + CTA.replace("{h}", "Let's build your brand.").replace("{p}", "Start with a 30-minute discovery call. We'll audit where you stand and show you the plan.") + "    </main>\n"

page("about.html", "About SeamlessFlow | Brand Growth Agency in NYC",
     "Over 10 years of making content. SeamlessFlow is a NYC brand growth agency that plans, films, posts, and runs ads to bring in customers.",
     about_main)
