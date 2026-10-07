"""Single source of truth for the site nav + footer.

Usage: python3 scripts/site_chrome.py index.html book-call.html ...
Each page must contain the markers <!-- NAV:START --> ... <!-- NAV:END -->
and <!-- FOOTER:START --> ... <!-- FOOTER:END -->. The homepage gets in-page
anchors (#how); every other page gets /#how so links work from anywhere.
"""
import sys

BOOK = "book-call.html"

INDUSTRIES = [
    ("roofing", "fa-home", "Roofing"),
    ("hvac", "fa-fan", "HVAC"),
    ("plumbing", "fa-wrench", "Plumbing"),
    ("electrical", "fa-plug", "Electrical"),
    ("remodeling", "fa-hammer", "Remodeling + Contractors"),
    ("junk-removal", "fa-truck-pickup", "Junk Removal"),
    ("moving", "fa-truck-moving", "Moving"),
    ("landscaping", "fa-leaf", "Landscaping"),
]

ADDONS = [
    ("ADDONS_ANCHOR", "fa-map-marker-alt", "Google SEO"),
    ("ADDONS_ANCHOR", "fa-store", "Google Business Profile"),
    ("ADDONS_ANCHOR", "fa-bolt", "Lead Follow-Up Automation"),
    ("ADDONS_ANCHOR", "fa-robot", "AI Chat Assistant"),
    ("ADDONS_ANCHOR", "fa-laptop-code", "Website Build"),
    ("ADDONS_ANCHOR", "fa-shield-alt", "Security Audits"),
]


def nav(p):
    desk_addons = "\n".join(
        f'                                <a href="{p}#addons" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600"><i class="fas {i} mr-2 text-blue-500"></i>{t}</a>'
        for h, i, t in ADDONS)
    mob_addons = "\n".join(
        f'''                    <a href="{p}#addons" class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors">
                        <i class="fas {i} mr-3 text-blue-500"></i>{t}
                    </a>''' for h, i, t in ADDONS)
    desk_ind = "\n".join(
        f'                                <a href="industries.html#{s}" class="block px-4 py-2 text-gray-700 hover:bg-blue-50 hover:text-blue-600"><i class="fas {i} mr-2 text-blue-500"></i>{t}</a>'
        for s, i, t in INDUSTRIES)
    mob_ind = "\n".join(
        f'''                    <a href="industries.html#{s}" class="block text-gray-700 hover:text-blue-600 hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors">
                        <i class="fas {i} mr-3 text-blue-500"></i>{t}
                    </a>''' for s, i, t in INDUSTRIES)
    home = "#home" if p == "" else "/"
    return f'''<!-- NAV:START -->
    <nav class="fixed top-0 w-full z-[60]" id="main-nav">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
            <div class="flex justify-center xl:justify-between items-center h-16 pr-16 xl:pr-0">
                <div class="flex items-center">
                    <a href="{home}" class="flex items-center">
                        <picture>
                            <source srcset="assets/website-homelogo.webp" type="image/webp">
                            <img src="assets/website homelogo.png"
                                 alt="SeamlessFlow.ai"
                                 class="h-8 sm:h-10"
                                 width="280"
                                 height="32"
                                 fetchpriority="high"
                                 decoding="async"
                                 style="width: auto; object-fit: contain; image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges;">
                        </picture>
                    </a>
                </div>
                <div class="hidden xl:block">
                    <div class="ml-10 flex items-baseline space-x-4">
                        <a href="{p}#how" class="text-gray-900 hover:text-blue-600 px-3 py-2">How It Works</a>
                        <div class="relative group">
                            <button class="text-gray-900 hover:text-blue-600 px-3 py-2 flex items-center">
                                Industries <i class="fas fa-chevron-down ml-1 text-sm"></i>
                            </button>
                            <div class="absolute top-full left-0 bg-white shadow-xl rounded-lg py-2 w-64 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
{desk_ind}
                                <a href="industries.html" class="block px-4 py-2 mt-1 border-t border-gray-100 text-blue-700 font-semibold hover:bg-blue-50">See all industries <i class="fas fa-arrow-right ml-1 text-xs"></i></a>
                            </div>
                        </div>
                        <a href="{p}#packages" class="text-gray-900 hover:text-blue-600 px-3 py-2">Packages</a>
                        <div class="relative group">
                            <button class="text-gray-900 hover:text-blue-600 px-3 py-2 flex items-center">
                                Add-Ons <i class="fas fa-chevron-down ml-1 text-sm"></i>
                            </button>
                            <div class="absolute top-full left-0 bg-white shadow-xl rounded-lg py-2 w-64 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
{desk_addons}
                            </div>
                        </div>
                        <a href="about.html" class="text-gray-900 hover:text-blue-600 px-3 py-2">About</a>
                        <a href="https://seamlessflow-hub.vercel.app/login" class="text-gray-600 hover:text-blue-600 px-3 py-2 text-sm font-medium">Login</a>
                        <a href="{BOOK}" class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg font-semibold shadow-sm hover:shadow-md transition-all">Book a Call</a>
                    </div>
                </div>
                <div class="xl:hidden absolute right-4" style="z-index: 80;">
                    <button class="hamburger" id="mobile-menu-button" aria-label="Toggle mobile menu">
                        <span></span>
                        <span></span>
                        <span></span>
                    </button>
                </div>
            </div>
        </div>
    </nav>

    <!-- Mobile Menu - Premium slide-in (outside nav to avoid z-index stacking context) -->
    <div id="mobile-menu" class="xl:hidden">
        <div class="flex justify-end px-6 pt-5 pb-2">
            <button id="mobile-menu-close" aria-label="Close menu" style="background:none;border:none;cursor:pointer;padding:8px;">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#374151" stroke-width="2.5" stroke-linecap="round">
                    <line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/>
                </svg>
            </button>
        </div>
        <div class="px-6 py-4 space-y-1">
            <a href="https://seamlessflow-hub.vercel.app/login" class="block text-gray-500 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium text-sm border-b border-gray-100 mb-2"><i class="fas fa-sign-in-alt mr-3 text-gray-400"></i>Login</a>
            <a href="{home}" class="block text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                <i class="fas fa-home mr-3 text-blue-500"></i>Home
            </a>
            <a href="{p}#how" class="block text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                <i class="fas fa-video mr-3 text-blue-500"></i>How It Works
            </a>
            <!-- Industries Collapsible -->
            <div class="mobile-dropdown">
                <button class="mobile-dropdown-btn w-full text-left text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-between">
                    <span><i class="fas fa-briefcase mr-3 text-blue-500"></i>Industries</span>
                    <i class="fas fa-chevron-right transition-transform duration-200"></i>
                </button>
                <div class="mobile-dropdown-content pl-6 space-y-1" style="max-height: 0; overflow-y: auto; transition: max-height 0.3s ease;">
{mob_ind}
                    <a href="industries.html" class="block text-blue-700 font-semibold hover:bg-blue-50 py-2 px-4 rounded-lg transition-colors">See all industries</a>
                </div>
            </div>
            <a href="{p}#packages" class="block text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                <i class="fas fa-layer-group mr-3 text-blue-500"></i>Packages
            </a>

            <!-- Add-Ons Collapsible -->
            <div class="mobile-dropdown">
                <button class="mobile-dropdown-btn w-full text-left text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors flex items-center justify-between">
                    <span><i class="fas fa-plus-circle mr-3 text-blue-500"></i>Add-Ons</span>
                    <i class="fas fa-chevron-right transition-transform duration-200"></i>
                </button>
                <div class="mobile-dropdown-content pl-6 space-y-1" style="max-height: 0; overflow-y: auto; transition: max-height 0.3s ease;">
{mob_addons}
                </div>
            </div>

            <a href="about.html" class="block text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                <i class="fas fa-user mr-3 text-blue-500"></i>About
            </a>
            <a href="faq.html" class="block text-gray-800 hover:text-blue-600 hover:bg-blue-50 py-3 px-4 rounded-lg font-medium transition-colors">
                <i class="fas fa-question-circle mr-3 text-blue-500"></i>FAQ
            </a>
            <div class="pt-4 border-t border-gray-100 mt-4 space-y-3">
                <a href="{BOOK}" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-4 rounded-lg block text-center font-bold shadow-lg hover:shadow-xl transition-all">
                    <i class="fas fa-calendar-check mr-2"></i>Book a Discovery Call
                </a>
                <a href="tel:+13477498146" class="block text-center text-gray-700 font-semibold py-2"><i class="fas fa-phone mr-2"></i>(347) 749-8146</a>
                <div class="flex justify-center items-center gap-6 pt-2">
                    <a href="https://instagram.com/seamlessflow.ai" target="_blank" rel="noopener noreferrer" class="text-gray-500 hover:text-pink-500 transition-colors" aria-label="Instagram">
                        <i class="fab fa-instagram text-xl"></i>
                    </a>
                    <a href="https://www.youtube.com/@SeamlessflowSEO" target="_blank" rel="noopener noreferrer" class="text-gray-500 hover:text-red-500 transition-colors" aria-label="YouTube">
                        <i class="fab fa-youtube text-xl"></i>
                    </a>
                </div>
            </div>
        </div>
    </div>
    <!-- NAV:END -->'''


def footer(p):
    what = [("#how", "Discovery Call + Brand Audit"), ("#how", "Content Plans + Scripts"),
            ("#how", "Shoot Days + Editing"), ("#how", "Posting + Analytics"),
            ("#how", "Ads on Proven Content"), ("#first-30", "Your First 30 Days")]
    what_li = "\n".join(f'                        <li><a href="{p}{h}" class="hover:text-white">{t}</a></li>' for h, t in what)
    add_li = "\n".join(f'                        <li><a href="{p}#addons" class="hover:text-white">{t}</a></li>' for h, _, t in ADDONS)
    return f'''<!-- FOOTER:START -->
    <footer class="bg-gray-950 text-white py-16 border-t border-gray-800">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8 sm:gap-6 md:gap-8">
                <div>
                    <h3 class="text-2xl font-bold mb-4">SeamlessFlow.ai</h3>
                    <p class="text-gray-300 mb-4">Brand growth through content that makes a difference.</p>
                    <div class="space-y-2 text-sm">
                        <div class="flex items-center text-blue-400">
                            <i class="fas fa-bolt mr-2"></i>
                            <span>Results in as little as 7 days</span>
                        </div>
                        <div class="flex items-center text-blue-400">
                            <i class="fas fa-phone mr-2"></i>
                            <span>(347) 749-8146</span>
                        </div>
                    </div>
                    <div class="mt-6">
                        <a href="{BOOK}" class="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg font-bold text-sm inline-block transition-colors">
                            <i class="fas fa-calendar-check mr-2"></i>Book a Discovery Call
                        </a>
                    </div>
                </div>

                <div>
                    <h4 class="font-bold mb-4">What We Do</h4>
                    <ul class="space-y-2 text-gray-300 text-sm">
{what_li}
                    </ul>
                </div>

                <div>
                    <h4 class="font-bold mb-4">Add-Ons</h4>
                    <ul class="space-y-2 text-gray-300 text-sm">
{add_li}
                    </ul>
                </div>

                <div>
                    <h4 class="font-bold mb-4">Company</h4>
                    <ul class="space-y-2 text-gray-300 text-sm">
                        <li><a href="about.html" class="hover:text-white">About Us</a></li>
                        <li><a href="industries.html" class="hover:text-white">Industries</a></li>
                        <li><a href="{p}#packages" class="hover:text-white">Packages</a></li>
                        <li><a href="faq.html" class="hover:text-white">FAQ</a></li>
                        <li><a href="{BOOK}" class="hover:text-white">Book a Discovery Call</a></li>
                        <li><a href="https://seamlessflow-hub.vercel.app/login" class="hover:text-white">Client Login</a></li>
                    </ul>
                    <div class="mt-4 space-y-2">
                        <a href="tel:+13477498146" class="flex items-center text-gray-300 hover:text-white">
                            <i class="fas fa-phone mr-2"></i>
                            <span class="font-bold">(347) 749-8146</span>
                        </a>
                        <a href="mailto:info@seamlessflow.ai" class="flex items-center text-gray-300 hover:text-white">
                            <i class="fas fa-envelope mr-2"></i>
                            <span class="text-sm">info@seamlessflow.ai</span>
                        </a>
                        <p class="flex items-center text-gray-400 text-sm"><i class="fas fa-map-marker-alt mr-2"></i>NYC based, available to travel</p>
                    </div>
                </div>
            </div>

            <div class="border-t border-gray-700 pt-8 mt-8">
                <div class="text-center text-gray-300 mb-4">
                    <div class="flex flex-wrap justify-center items-center gap-4 text-sm">
                        <span class="flex items-center">
                            <i class="fas fa-video mr-2 text-blue-400"></i>
                            Shoot, Edit, Post, Ads
                        </span>
                        <span class="flex items-center">
                            <i class="fas fa-pen mr-2 text-blue-400"></i>
                            Scripts Written For You
                        </span>
                        <span class="flex items-center">
                            <i class="fas fa-map-marker-alt mr-2 text-blue-400"></i>
                            NYC Based, We Travel
                        </span>
                    </div>
                </div>
                <div class="flex justify-center gap-6 mb-4">
                    <a href="https://linkedin.com/company/seamlessflow" target="_blank" rel="noopener noreferrer" class="text-gray-400 hover:text-white transition-colors" aria-label="LinkedIn"><i class="fab fa-linkedin text-xl"></i></a>
                    <a href="https://instagram.com/seamlessflow.ai" target="_blank" rel="noopener noreferrer" class="text-gray-400 hover:text-white transition-colors" aria-label="Instagram"><i class="fab fa-instagram text-xl"></i></a>
                    <a href="https://www.youtube.com/@SeamlessflowSEO" target="_blank" rel="noopener noreferrer" class="text-gray-400 hover:text-white transition-colors" aria-label="YouTube"><i class="fab fa-youtube text-xl"></i></a>
                    <a href="https://x.com/seamlessflowai" target="_blank" rel="noopener noreferrer" class="text-gray-400 hover:text-white transition-colors" aria-label="X"><i class="fab fa-x-twitter text-xl"></i></a>
                </div>
                <div class="text-center text-gray-400 text-sm">
                    <p>&copy; 2026 SeamlessFlow.ai. All rights reserved. | <a href="privacy-policy.html" class="hover:text-white">Privacy Policy</a> | <a href="terms-of-service.html" class="hover:text-white">Terms of Service</a> | <a href="cookies-policy.html" class="hover:text-white">Cookies Policy</a></p>
                </div>
            </div>
        </div>
    </footer>
    <!-- FOOTER:END -->'''


def swap(text, start, end, new):
    a, b = text.index(start), text.index(end) + len(end)
    return text[:a] + new + text[b:]


if __name__ == "__main__":
    for path in sys.argv[1:]:
        t = open(path).read()
        p = "" if path.endswith("index.html") and "/" not in path else "/"
        t = swap(t, "<!-- NAV:START -->", "<!-- NAV:END -->", nav(p))
        t = swap(t, "<!-- FOOTER:START -->", "<!-- FOOTER:END -->", footer(p))
        open(path, "w").write(t)
        print("updated", path)
