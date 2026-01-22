// ============================================
// SEAMLESSFLOW CHAT WIDGET - GPCT FUNNEL
// ============================================

(function() {
    const WEBHOOK_URL = 'https://seamlessflow1.app.n8n.cloud/webhook/chatbot-lead';
    const STORAGE_KEY = 'sf_chat_submitted';
    const FAILED_LEADS_KEY = 'sf_chat_failed_leads';

    // Check if user already submitted
    function hasAlreadySubmitted() {
        try {
            return localStorage.getItem(STORAGE_KEY) !== null;
        } catch (e) {
            return false;
        }
    }

    // Save failed lead to localStorage for retry
    function saveFailedLead(payload) {
        try {
            const failed = JSON.parse(localStorage.getItem(FAILED_LEADS_KEY) || '[]');
            failed.push({ ...payload, failed_at: new Date().toISOString() });
            localStorage.setItem(FAILED_LEADS_KEY, JSON.stringify(failed));
        } catch (e) {
            console.error('Could not save failed lead:', e);
        }
    }

    // Mark user as submitted
    function markAsSubmitted(email) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify({
                email: email,
                submitted_at: new Date().toISOString()
            }));
        } catch (e) {
            console.error('Could not save submission status:', e);
        }
    }

    // Fetch with timeout
    function fetchWithTimeout(url, options, timeout = 10000) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);
        return fetch(url, { ...options, signal: controller.signal })
            .finally(() => clearTimeout(timeoutId));
    }

    const chatState = {
        step: 0,
        bypassAttempts: 0,
        qualified: false,
        data: {
            goal: '',
            businessType: '',
            challenge: '',
            timeline: '',
            teamSize: '',
            email: '',
            wantsCall: false
        },
        transcript: []
    };

    const bypassPatterns = [
        /skip/i, /next/i, /later/i, /don't want/i, /no thanks/i,
        /not now/i, /pass/i, /nevermind/i, /forget it/i,
        /just tell me/i, /can you just/i, /i just want/i,
        /^no$/i, /^nah$/i, /^nope$/i, /why do you need/i
    ];

    const bypassResponses = [
        "I get it - no one likes forms. But these questions help me figure out if we can actually help you. What's your main goal right now?",
        "Fair enough! Just trying to make sure I connect you with the right info. What are you trying to achieve?",
        "No pressure at all. I just want to make sure I'm not wasting your time. What's the main thing you're working on?"
    ];

    const conversationFlow = [
        {
            message: "Hey! I'm Jamie 🤖 What are you looking to improve today?",
            field: 'goal',
            quickReplies: [
                "Get more customers (SEO)",
                "Automate my business (AI/Bots)",
                "Need an AI Budtender",
                "Protect my business (Security)"
            ],
            required: true,
            validateAs: 'goal'
        },
        {
            message: "Nice. What type of cannabis business are you?",
            field: 'businessType',
            quickReplies: [
                "Dispensary / Retailer",
                "Cultivator / Grower",
                "Processor / Manufacturer",
                "Distributor / Delivery"
            ],
            required: true,
            validateAs: 'businessType'
        },
        {
            message: "Got it. What's the biggest thing holding you back?",
            field: 'challenge',
            quickReplies: [],
            required: true,
            validateAs: 'challenge'
        },
        {
            message: "How soon are you looking to fix this?",
            field: 'timeline',
            quickReplies: [
                "ASAP - it's urgent",
                "Next 30 days",
                "Next few months",
                "Just researching"
            ],
            required: true,
            validateAs: 'timeline'
        },
        {
            message: "Quick one - how big is your team?",
            field: 'teamSize',
            quickReplies: [
                "Just me",
                "2-5 people",
                "6-20 people",
                "20+ people"
            ],
            required: true,
            validateAs: 'teamSize'
        },
        {
            message: "Almost done! What's the best email to reach you?",
            field: 'email',
            placeholder: "your@email.com",
            required: true,
            validateAs: 'email'
        },
        {
            message: "",
            field: 'wantsCall',
            quickReplies: [
                "Email me first",
                "Let's do a quick call"
            ],
            required: true,
            validateAs: 'cta'
        }
    ];

    const challengesByGoal = {
        seo: ["Competitors outranking us", "Not showing on Google Maps", "Bad or few reviews", "Website doesn't convert"],
        automation: ["Too much manual work", "Compliance paperwork overwhelming", "Can't keep up with orders", "Staff doing tasks bots could do"],
        budtender: ["Staff can't answer all product questions", "Inconsistent recommendations", "Customers overwhelmed by choices", "High turnover / training costs"],
        security: ["Worried about data breaches", "Compliance / audit concerns", "Don't know our vulnerabilities", "Need to protect customer data"]
    };

    const ctaByGoal = {
        seo: "Perfect! Want a free visibility audit on a quick call, or should I email you first?",
        automation: "Perfect! Want to discuss automation options on a quick call, or email first?",
        budtender: "Perfect! Want a quick AI Budtender demo call, or should I email you info first?",
        security: "Perfect! Want a free security assessment call, or should I email you first?"
    };

    function getGoalType(goalText) {
        const g = goalText.toLowerCase();
        if (g.includes('seo') || g.includes('customer')) return 'seo';
        if (g.includes('automate') || g.includes('bot')) return 'automation';
        if (g.includes('budtender')) return 'budtender';
        if (g.includes('security') || g.includes('protect')) return 'security';
        return 'seo';
    }

    const validators = {
        goal: (text) => text.length >= 2 ? null : "Just tap one of the options!",
        businessType: (text) => text.length >= 2 ? null : "What type of business are you?",
        challenge: (text) => text.length >= 2 ? null : "What's the main thing holding you back?",
        timeline: (text) => text.length >= 2 ? null : "Just give me a rough idea of timing.",
        teamSize: (text) => text.length >= 1 ? null : "How big is your team?",
        email: (text) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(text.trim()) ? null : "I need a valid email to send the report!",
        cta: () => null
    };

    // Inject widget HTML
    function injectWidget() {
        const widgetHTML = `
        <div class="chat-widget">
            <div class="chat-window" id="chatWindow">
                <div class="chat-header">
                    <div class="chat-header-avatar">
                        <svg viewBox="0 0 24 24"><path d="M12 2a2 2 0 012 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 017 7h1a1 1 0 011 1v3a1 1 0 01-1 1h-1v1a2 2 0 01-2 2H5a2 2 0 01-2-2v-1H2a1 1 0 01-1-1v-3a1 1 0 011-1h1a7 7 0 017-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 012-2zM7.5 13a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm9 0a1.5 1.5 0 100 3 1.5 1.5 0 000-3zM12 17c-1.5 0-2.5-.5-3-1h6c-.5.5-1.5 1-3 1z"/></svg>
                    </div>
                    <div class="chat-header-info">
                        <h3>Jamie</h3>
                        <p>SeamlessFlow Assistant</p>
                    </div>
                    <button class="chat-close-mobile" id="chatClose">
                        <svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
                    </button>
                </div>
                <div class="chat-messages" id="chatMessages"></div>
                <div class="chat-input-area">
                    <div class="chat-input-wrapper">
                        <input type="text" class="chat-input" id="chatInput" placeholder="Type your message..." autocomplete="off">
                        <button class="chat-send" id="chatSend">
                            <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
                        </button>
                    </div>
                </div>
            </div>
            <button class="chat-toggle" id="chatToggle" title="Chat with Jamie">
                <svg viewBox="0 0 24 24"><path d="M12 2a2 2 0 012 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 017 7h1a1 1 0 011 1v3a1 1 0 01-1 1h-1v1a2 2 0 01-2 2H5a2 2 0 01-2-2v-1H2a1 1 0 01-1-1v-3a1 1 0 011-1h1a7 7 0 017-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 012-2zM7.5 13a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm9 0a1.5 1.5 0 100 3 1.5 1.5 0 000-3zM12 17c-1.5 0-2.5-.5-3-1h6c-.5.5-1.5 1-3 1z"/></svg>
            </button>
        </div>`;

        document.body.insertAdjacentHTML('beforeend', widgetHTML);
    }

    function initWidget() {
        injectWidget();

        const chatToggle = document.getElementById('chatToggle');
        const chatWindow = document.getElementById('chatWindow');
        const chatMessages = document.getElementById('chatMessages');
        const chatInput = document.getElementById('chatInput');
        const chatSend = document.getElementById('chatSend');
        const chatClose = document.getElementById('chatClose');

        chatToggle.addEventListener('click', () => {
            chatWindow.classList.add('active');
            chatToggle.classList.add('hidden');
            if (chatState.step === 0 && chatState.transcript.length === 0) {
                setTimeout(() => startConversation(), 500);
            }
            chatInput.focus();
        });

        chatClose.addEventListener('click', () => {
            chatWindow.classList.remove('active');
            chatToggle.classList.remove('hidden');
        });

        function startConversation() {
            // Check if returning user
            if (hasAlreadySubmitted()) {
                const welcomeBack = "Welcome back! 👋 We already have your info on file. Need to update something or have a question?";
                addBotMessage(welcomeBack, [
                    "Start fresh conversation",
                    "Call (347) 749-8146",
                    "Email info@seamlessflow.ai"
                ]);
                logTranscript('bot', welcomeBack);
                chatState.isReturningUser = true;
                return;
            }

            const first = conversationFlow[0];
            addBotMessage(first.message, first.quickReplies);
            logTranscript('bot', first.message);
            chatInput.placeholder = first.placeholder || 'Type or select...';
        }

        function logTranscript(sender, message) {
            chatState.transcript.push({
                sender, message,
                timestamp: new Date().toISOString()
            });
        }

        function isBypassAttempt(text) {
            return bypassPatterns.some(p => p.test(text.trim()));
        }

        function addBotMessage(text, quickReplies = null) {
            const typing = document.createElement('div');
            typing.className = 'chat-typing';
            typing.innerHTML = '<span></span><span></span><span></span>';
            chatMessages.appendChild(typing);
            scrollToBottom();

            setTimeout(() => {
                typing.remove();
                const msg = document.createElement('div');
                msg.className = 'chat-message bot';
                msg.textContent = text;
                chatMessages.appendChild(msg);

                if (quickReplies && quickReplies.length > 0) {
                    const replies = document.createElement('div');
                    replies.className = 'chat-quick-replies';
                    quickReplies.forEach(reply => {
                        const btn = document.createElement('button');
                        btn.className = 'chat-quick-reply';
                        btn.textContent = reply;
                        btn.addEventListener('click', () => handleUserInput(reply));
                        replies.appendChild(btn);
                    });
                    chatMessages.appendChild(replies);
                }
                scrollToBottom();
            }, 800);
        }

        function addUserMessage(text) {
            const msg = document.createElement('div');
            msg.className = 'chat-message user';
            msg.textContent = text;
            chatMessages.appendChild(msg);
            scrollToBottom();
        }

        function handleUserInput(text) {
            if (!text.trim()) return;

            // Handle returning user options
            if (chatState.isReturningUser) {
                addUserMessage(text);
                logTranscript('user', text);

                const qr = chatMessages.querySelector('.chat-quick-replies');
                if (qr) qr.remove();

                if (text.toLowerCase().includes('start fresh')) {
                    chatState.isReturningUser = false;
                    setTimeout(() => {
                        const first = conversationFlow[0];
                        addBotMessage(first.message, first.quickReplies);
                        logTranscript('bot', first.message);
                        chatInput.placeholder = first.placeholder || 'Type or select...';
                    }, 500);
                } else if (text.toLowerCase().includes('call')) {
                    setTimeout(() => {
                        addBotMessage("Give us a ring at (347) 749-8146 - we're here to help! 📞");
                    }, 500);
                    chatInput.disabled = true;
                    chatSend.disabled = true;
                } else if (text.toLowerCase().includes('email')) {
                    setTimeout(() => {
                        addBotMessage("Shoot us an email at info@seamlessflow.ai and we'll get back to you ASAP! 📧");
                    }, 500);
                    chatInput.disabled = true;
                    chatSend.disabled = true;
                }
                return;
            }

            const currentStep = conversationFlow[chatState.step];

            addUserMessage(text);
            logTranscript('user', text);

            if (currentStep.required && isBypassAttempt(text)) {
                chatState.bypassAttempts++;
                const response = bypassResponses[Math.min(chatState.bypassAttempts - 1, bypassResponses.length - 1)];
                setTimeout(() => {
                    addBotMessage(response);
                    logTranscript('bot', response);
                }, 500);
                chatInput.value = '';
                return;
            }

            const validator = validators[currentStep.validateAs];
            const error = validator ? validator(text) : null;
            if (error && currentStep.required) {
                setTimeout(() => {
                    addBotMessage(error);
                    logTranscript('bot', error);
                }, 500);
                chatInput.value = '';
                return;
            }

            const qr = chatMessages.querySelector('.chat-quick-replies');
            if (qr) qr.remove();

            if (currentStep.field === 'wantsCall') {
                chatState.data.wantsCall = text.toLowerCase().includes('call');
            } else {
                chatState.data[currentStep.field] = text.trim();
            }

            if (currentStep.field === 'goal') {
                const goalType = getGoalType(text);
                chatState.goalType = goalType;
                conversationFlow[2].quickReplies = challengesByGoal[goalType];
                conversationFlow[6].message = ctaByGoal[goalType];

                if (goalType === 'budtender') {
                    chatState.data.businessType = 'Dispensary / Retailer';
                    chatState.step = 2;
                    chatState.bypassAttempts = 0;
                    chatInput.value = '';
                    const nextStep = conversationFlow[chatState.step];
                    setTimeout(() => {
                        addBotMessage("Perfect - dispensary it is! " + nextStep.message, nextStep.quickReplies);
                        logTranscript('bot', "Perfect - dispensary it is! " + nextStep.message);
                        chatInput.placeholder = nextStep.placeholder || 'Type or select...';
                    }, 500);
                    return;
                }
            }

            chatState.step++;
            chatState.bypassAttempts = 0;
            chatInput.value = '';

            if (chatState.step >= conversationFlow.length) {
                submitLead();
                return;
            }

            const nextStep = conversationFlow[chatState.step];
            let message = nextStep.message;

            setTimeout(() => {
                addBotMessage(message, nextStep.quickReplies);
                logTranscript('bot', message);
                chatInput.placeholder = nextStep.placeholder || 'Type or select...';
            }, 500);
        }

        async function submitLead() {
            const sendingMsg = "Got it! Sending this over to the team now...";
            addBotMessage(sendingMsg);
            logTranscript('bot', sendingMsg);

            const urgentTimelines = ['asap', 'urgent', '30 days', 'next 30'];
            chatState.qualified = urgentTimelines.some(t =>
                chatState.data.timeline.toLowerCase().includes(t)
            );

            const payload = {
                ...chatState.data,
                qualified: chatState.qualified,
                source: 'website_chatbot_gpct',
                timestamp: new Date().toISOString(),
                page_url: window.location.href,
                transcript: chatState.transcript,
                transcript_text: chatState.transcript.map(t =>
                    `[${t.sender.toUpperCase()}] ${t.message}`
                ).join('\n'),
                bypass_attempts: chatState.bypassAttempts,
                is_mobile: window.innerWidth <= 768
            };

            try {
                await fetchWithTimeout(WEBHOOK_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                }, 10000);

                // Mark as submitted to prevent repeat spam
                markAsSubmitted(chatState.data.email);

                let finalMsg;
                if (chatState.data.wantsCall) {
                    finalMsg = "Perfect! Check your email - you'll get a link to book a time that works for you. Talk soon!";
                } else {
                    finalMsg = `You're all set! We'll put together some insights and send them to ${chatState.data.email}. Keep an eye on your inbox!`;
                }

                setTimeout(() => {
                    addBotMessage(finalMsg);
                    logTranscript('bot', finalMsg);
                }, 1500);

            } catch (error) {
                console.error('Webhook error:', error);

                // Save lead locally so it's not lost
                saveFailedLead(payload);

                // Honest error message with contact options
                setTimeout(() => {
                    const errorMsg = "Hmm, something went wrong on our end. Your info is saved locally. Please reach out directly:";
                    addBotMessage(errorMsg);
                    logTranscript('bot', errorMsg);

                    setTimeout(() => {
                        addBotMessage("📞 Call: (347) 749-8146\n📧 Email: info@seamlessflow.ai\n\nSorry for the trouble - we'll make it right!");
                    }, 800);
                }, 1500);
            }

            chatInput.disabled = true;
            chatSend.disabled = true;
            chatInput.placeholder = 'Conversation complete';
        }

        chatSend.addEventListener('click', () => handleUserInput(chatInput.value));
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleUserInput(chatInput.value);
        });

        function scrollToBottom() {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    // Init when DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWidget);
    } else {
        initWidget();
    }
})();
