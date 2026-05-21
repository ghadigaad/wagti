"""English / Najdi Arabic for Wagti."""

from __future__ import annotations

from typing import Any

LOCALES = frozenset({"en", "ar"})
COOKIE_NAME = "sf_locale"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365

_MSG: dict[str, dict[str, str]] = {
    # ─── Nav / chrome ─────────────────────────────────────────
    "brand.tagline": {
        "en": "Track your day. Find your focus.",
        "ar": "رتّب يومك وخلّ تركيزك ثابت.",
    },
    "nav.tasks": {"en": "Tasks", "ar": "المهام"},
    "nav.focus": {"en": "Focus", "ar": "التركيز"},
    "nav.insights": {"en": "Insights", "ar": "الإحصائيات"},
    "nav.guest": {"en": "Guest", "ar": "ضيف"},
    "nav.signup_title": {"en": "Open a free account", "ar": "سجّل مجانًا"},
    "nav.logout_title": {"en": "Sign out", "ar": "تسجيل خروج"},
    "nav.theme_title": {"en": "Change theme", "ar": "غيّر الشكل"},
    "nav.menu_aria": {"en": "Menu", "ar": "القائمة"},
    "nav.lang_switch_en": {"en": "English", "ar": "English"},
    "nav.lang_switch_ar": {"en": "العربية", "ar": "العربية"},
    "guest.banner": {
        "en": "You’re in a guest session so nothing is saved for later",
        "ar": "أنت داخل كضيف، يعني شغلك ما ينحفظ بعد ما تطلع",
    },
    "guest.banner_link": {"en": "Get a free account", "ar": "افتح حساب مجاني"},
    "guest.banner_suffix": {"en": "if you want to keep it.", "ar": "إذا ودّك تحفظ شغلك."},
    "footer.tagline": {
        "en": "Small steps. Steady focus.",
        "ar": "خطوة خطوة… وتركيزك يصير أحسن.",
    },
    # ─── Landing ──────────────────────────────────────────────
    "landing.title": {
        "en": "Wagti | Smart Focus & Productivity Tracker",
        "ar": "وقتي | لتنظيم وقتك وتركيزك",
    },
    "landing.badge": {"en": "Smart focus, your way", "ar": "تركيز ذكي… بطريقتك"},
    "landing.hero_l1": {"en": "Your time, your rules.", "ar": "وقتك على كيفك."},
    "landing.hero_l2": {
        "en": "Dial in the focus you want.",
        "ar": "ادخل مود التركيز اللي يناسبك.",
    },
    "landing.sub": {
        "en": "Tasks, Pomodoro, and a little insight into how you actually work — in one place.",
        "ar": "مهام، بومودورو، وفهم لطريقتك بالشغل… كله بمكان واحد.",
    },
    "landing.based_on": {
        "en": "Pulled from what you really do, not a guess",
        "ar": "على وش تسوّي فعلًا، مو تخمين",
    },
    "landing.cta_register": {"en": "Get Started Free", "ar": "ابدأ مجانًا"},
    "landing.cta_guest": {"en": "Try as Guest", "ar": "جرّبه كضيف"},
    "landing.note": {"en": "Been here before?", "ar": "عندك حساب؟"},
    "landing.sign_in": {"en": "Sign in", "ar": "سجّل دخول"},
    "landing.hero_focus_score": {"en": "Focus score", "ar": "مستوى تركيزك"},
    "landing.hero_good": {"en": "On track", "ar": "أمورك تمام"},
    "landing.hero_warning": {
        "en": "Only 12 min in today — try a 25 min block to bump it up",
        "ar": "اليوم ما أخذت إلا ١٢ دقيقة… جرّب جلسة ٢٥ دقيقة وشوف الفرق.",
    },
    "landing.hero_ai": {"en": "Next smart guess", "ar": "اقتراح ذكي لك"},
    "landing.hero_ai_text": {
        "en": "Picks up your rhythm and nudges you toward a good time window.",
        "ar": "يفهم وقت نشاطك ويقترح عليك أفضل وقت تركز فيه.",
    },
    "landing.features_title": {
        "en": "What you get in one app",
        "ar": "وش يعطيك التطبيق؟",
    },
    "landing.f1_title": {"en": "Sort your time", "ar": "رتّب وقتك"},
    "landing.f1_text": {
        "en": "Name the task, pick a time box, and see what it really took.",
        "ar": "اكتب المهمة، حدّد وقتها، وشوف كم أخذت منك فعلًا.",
    },
    "landing.f2_title": {"en": "Deep focus timer", "ar": "مؤقت تركيز"},
    "landing.f2_text": {
        "en": "Pomodoro built in with real breaks.",
        "ar": "بومودورو يساعدك تركز بدون ما تضغط نفسك.",
    },
    "landing.f3_title": {"en": "Your insight board", "ar": "كل شي واضح قدّامك"},
    "landing.f3_text": {
        "en": "See your day, your mix of work types, and when the flow shows up.",
        "ar": "شوف يومك، وش أكثر شي يشغلك، ومتى يكون تركيزك بأفضل حالاته.",
    },
    "landing.f4_title": {"en": "Focus score", "ar": "مستوى تركيزك"},
    "landing.f4_text": {
        "en": "A simple 0 to 100 read on time, tasks, and consistency.",
        "ar": "درجة بسيطة من ٠ لـ١٠٠ توضّح التزامك وتركيزك.",
    },
    "landing.f5_title": {"en": "Heads up when you drift", "ar": "ينبّهك إذا تشتّت"},
    "landing.f5_text": {
        "en": "A small ping when you slip under your own usual line.",
        "ar": "إذا حس إن تركيزك نازل عن المعتاد يعطيك تنبيه بسيط.",
    },
    "landing.f6_title": {"en": "Smart timing hint", "ar": "أفضل وقت لك"},
    "landing.f6_text": {
        "en": "Looks at past runs and nudges you at hours that worked before.",
        "ar": "يتعلّم من جلساتك السابقة ويقترح عليك وقت يناسبك.",
    },
    "landing.final_title": {"en": "Start small today", "ar": "ابدأ اليوم حتى لو بشي بسيط"},
    "landing.final_sub": {"en": "Free forever, no card needed.", "ar": "مجاني بالكامل وبدون تعقيد."},
    "landing.cta_create": {"en": "Create free account", "ar": "افتح حساب مجاني"},
    "landing.final_note": {"en": "Less noise, more focus.", "ar": "إزعاج أقل… وتركيز أكثر."},
    # ─── Tasks ───────────────────────────────────────────────
    "tasks.title_page": {"en": "Tasks — Wagti", "ar": "المهام — وقتي"},
    "tasks.header": {"en": "This is your queue", "ar": "هذي مهامك"},
    "tasks.sub": {
        "en": "Drop a task, pick a slot, and watch the clock tell the truth.",
        "ar": "أضف مهمة، حدّد وقتها، وخلك صادق مع وقتك.",
    },
    "tasks.new_task": {"en": "New task", "ar": "مهمة جديدة"},
    "tasks.task_name": {"en": "What is it called?", "ar": "وش اسم المهمة؟"},
    "tasks.placeholder_name": {
        "en": "e.g. read chapter 3",
        "ar": "مثال: مراجعة الفصل الثالث",
    },
    "tasks.category": {"en": "Category", "ar": "التصنيف"},
    "tasks.goal_min": {"en": "Target (min)", "ar": "الوقت المتوقع"},
    "tasks.add": {"en": "Add to list", "ar": "أضف المهمة"},
    "tasks.stat_active": {"en": "Running now", "ar": "شغّالة الحين"},
    "tasks.stat_completed": {"en": "Done today", "ar": "خلصت اليوم"},
    "tasks.stat_time": {"en": "On task today", "ar": "مهامك اليوم"},
    "tasks.your_tasks": {"en": "The list", "ar": "اللستة"},
    "tasks.filter_all": {"en": "All", "ar": "الكل"},
    "tasks.filter_pending": {"en": "Waiting", "ar": "تنتظرك"},
    "tasks.filter_active": {"en": "In progress", "ar": "شغّال عليها"},
    "tasks.filter_completed": {"en": "Done", "ar": "مخلّصة"},
    "tasks.filter_cat_all": {"en": "Every kind", "ar": "كل شي"},
    "tasks.empty": {
        "en": "Empty list. Add one up top to see it move.",
        "ar": "اللستة فاضية للحين 👀",
    },
    # ─── Focus ───────────────────────────────────────────────
    "focus.title_page": {"en": "Deep Focus — Wagti", "ar": "تركيز عميق — وقتي"},
    "focus.header": {"en": "Heads down time", "ar": "خلّك مركز"},
    "focus.sub": {
        "en": "Pick a block and let the rhythm carry you.",
        "ar": "ابدأ الجلسة وخلك بالمود.",
    },
    "focus.mode_pom": {"en": "Focus", "ar": "تركيز"},
    "focus.duration_label": {"en": "Session length", "ar": "مدة الجلسة"},
    "focus.duration_unit": {"en": "min", "ar": "دقيقة"},
    "focus.duration_hint": {"en": "1–60 min", "ar": "من ١ إلى ٦٠ دقيقة"},
    "focus.mode_short": {"en": "Quick 5m break", "ar": "راحة ٥ دقايق"},
    "focus.mode_long": {"en": "Long 15m break", "ar": "راحة طويلة ١٥ دقيقة"},
    "focus.label_focus": {"en": "In the zone", "ar": "في الجو"},
    "focus.label_short": {"en": "Breathe", "ar": "رِحت لحظة"},
    "focus.label_long": {"en": "Recharge", "ar": "طوّل النفس"},
    "focus.start": {"en": "Start", "ar": "ابدأ"},
    "focus.pause": {"en": "Pause", "ar": "وقف"},
    "focus.resume": {"en": "Resume", "ar": "كمّل"},
    "focus.reset": {"en": "Reset", "ar": "إعادة"},
    "focus.sound_alerts": {"en": "Chime when the block ends", "ar": "صوت لما ينتهي الوقت"},
    "focus.alert": {
        "en": "You slipped away. Come back when you can",
        "ar": "طلعت من الجلسة 👀 ارجع كمّل إذا فضيت",
    },
    "focus.tips_title": {"en": "How a Pomodoro run works", "ar": "كيف بومودورو يمشي"},
    "focus.tip1": {"en": "Go in for", "ar": "ادخل"},
    "focus.tip1b": {"en": "your block", "ar": "مدة جلستك"},
    "focus.tip1c": {"en": "with the tab on this", "ar": "وخلك على نفس النافذه"},
    "focus.tip2": {"en": "Then grab a", "ar": "بعدها"},
    "focus.tip2b": {"en": "5 min", "ar": "٥ د"},
    "focus.tip2c": {"en": "off-screen breather", "ar": "راحة بعيد"},
    "focus.tip3": {"en": "After four sprints, take a", "ar": "بعد ٤ دوّرات"},
    "focus.tip3b": {"en": "15 min", "ar": "١٥ د"},
    "focus.tip3c": {"en": "real long break", "ar": "راحة فعلية"},
    "focus.tip4": {"en": "Four rounds make one set", "ar": "٤ فوق بعض = دفعة واضحة"},
    "focus.stats_title": {"en": "This run so far", "ar": "الحين بجلسة"},
    "focus.pom_today": {"en": "Pomos today", "ar": "بومودورات اليوم"},
    "focus.total_focus": {"en": "Time in focus this visit", "ar": "دقايق تركيزك هالمرّة"},
    "focus.current_mode": {"en": "You’re in", "ar": "وضعك:"},
    "focus.doc_title": {"en": "Deep Focus — Wagti", "ar": "تركيز عميق — وقتي"},
    "focus.title_flash": {"en": "⚠️ stay here", "ar": "⚠️ خلك هنا"},
    # ─── Dashboard ──────────────────────────────────────────
    "dash.title_page": {"en": "Insights — Wagti", "ar": "الإحصائيات — وقتي"},
    "dash.header": {"en": "Your readout", "ar": "وش وضعك اليوم؟"},
    "dash.sub": {
        "en": "A simple view of how your days line up.",
        "ar": "نظرة سريعة على وقتك وتركيزك.",
    },
    "dash.today_focus": {"en": "Focus so far today", "ar": "تركيزك اليوم"},
    "dash.tasks_today": {"en": "Tasks you closed", "ar": "المهام اللي خلصتها"},
    "dash.alltime": {"en": "All-in hours", "ar": "إجمالي الساعات"},
    "dash.focus_score": {"en": "Focus score", "ar": "مستوى التركيز"},
    "dash.focus_alerts": {"en": "Heads up", "ar": "تنبيهات لك"},
    "dash.chart_daily": {"en": "Last 7 days in view", "ar": "آخر أسبوع"},
    "dash.chart_cat": {"en": "How today split", "ar": "تقسيمة هاليوم"},
    "dash.chart_hourly": {
        "en": "When you show up (all time)",
        "ar": "وين الوقت الافضل (عمومًا)",
    },
    "dash.no_cat_data": {
        "en": "Nothing here yet. Start a run and it fills in",
        "ar": "فاضي. ابدأ جلسه ",
    },
    "dash.ai_pred": {"en": "Next good window", "ar": "أفضل وقت لك غالبًا"},
    "dash.rec_title": {"en": "Notes for you", "ar": "ملاحظات لك"},
    "dash.loading_rec": {"en": "Pulling ideas…", "ar": "نظل نجيب لك اقتراحات…"},
    "dash.breakdown": {"en": "Where the points go", "ar": "وين راحت النقاط"},
    "dash.br_focus": {"en": "On-task time", "ar": "وقت على المهمة"},
    "dash.br_tasks": {"en": "Tasks bagged", "ar": "مهام محسومة"},
    "dash.br_cons": {"en": "Showed up (7d)", "ar": "تكرار (٧ أيام)"},
    "dash.chart_minutes": {"en": "min", "ar": "دقايق"},
    "dash.pts": {"en": "pts", "ar": "نقطة"},
    # ─── Auth ───────────────────────────────────────────────
    "auth.back_title": {"en": "Back home", "ar": "رجوع"},
    "auth.register_title": {"en": "Register — Wagti", "ar": "تسجيل — وقتي"},
    "auth.login_title": {"en": "Login — Wagti", "ar": "دخول — وقتي"},
    "auth.create_title": {"en": "Set up your space", "ar": "سوّ حسابك"},
    "auth.create_sub": {"en": "Takes a moment, then you’re in", "ar": "دقيقة وتدخل معنا"},
    "auth.welcome": {"en": "Good to see you", "ar": "يا هلا فيك"},
    "auth.signin_sub": {
        "en": "Use the name and password you picked",
        "ar": "نفس اسمك وكلمة السر",
    },
    "auth.username": {"en": "Username", "ar": "اسم المستخدم"},
    "auth.ph_user": {"en": "What we should call you", "ar": "كيف تحب نناديك"},
    "auth.email": {"en": "Email", "ar": "الإيميل"},
    "auth.ph_email": {"en": "you@example.com", "ar": "you@example.com"},
    "auth.password": {"en": "Password", "ar": "كلمة المرور"},
    "auth.ph_password": {"en": "Your password", "ar": "كلمة السر"},
    "auth.ph_create_pw": {"en": "Make it hard to guess", "ar": "خله صعب تخمينه"},
    "auth.confirm": {"en": "Confirm it", "ar": "أكد كلمة المرور"},
    "auth.ph_confirm": {"en": "Type it again", "ar": "عيدها مرة"},
    "auth.req_len": {"en": "8+ characters", "ar": "٨ أحرف فوق"},
    "auth.req_upper": {"en": "One cap letter", "ar": "حرف كبير"},
    "auth.req_digit": {"en": "One number", "ar": "رقم"},
    "auth.req_special": {"en": "One symbol (!@#…)", "ar": "رمز (!@#…)"},
    "auth.sign_in": {"en": "Sign in", "ar": "دخول"},
    "auth.create_account": {"en": "Create it", "ar": "إنشاء الحساب"},
    "auth.or": {"en": "or", "ar": "أو"},
    "auth.guest": {"en": "Peek as guest", "ar": "تفرّج كضيف"},
    "auth.have_account": {"en": "Have an account?", "ar": "عندك حساب؟"},
    "auth.sign_in_link": {"en": "Sign in", "ar": "تسجيل دخول"},
    "auth.no_account": {"en": "New here?", "ar": "جديد؟"},
    "auth.create_free": {"en": "Open one free", "ar": "سجّل مجانا"},
    "auth.pw_weak": {"en": "Soft", "ar": "ضعيف"},
    "auth.pw_fair": {"en": "Okay", "ar": "يمشي"},
    "auth.pw_good": {"en": "Nice", "ar": "حلو"},
    "auth.pw_strong": {"en": "Solid", "ar": "قوي"},
    "auth.pw_match_ok": {"en": "✓ same words", "ar": "✓ نفس الكلمتين"},
    "auth.pw_match_bad": {"en": "✗ not the same", "ar": "✗ مو نفس بعض"},
    # API / flash (app.py)
    "api.task_name_required": {
        "en": "We need a name for that task",
        "ar": "لازم تسمي المهمة",
    },
    "api.task_deleted": {"en": "Gone from the list", "ar": "انشالت من اللستة"},
    "api.task_completed": {"en": "That one’s already done", "ar": "هذي منتهية أصلًا"},
    "api.task_not_active": {
        "en": "Nothing is running on that one",
        "ar": "ما اشتغل عليها شي",
    },
    "flash.login_bad": {
        "en": "That name or password didn’t match",
        "ar": "الاسم أو السر مو مطابقين",
    },
    "flash.all_required": {"en": "Fill every field", "ar": "عبي الحقول كلها"},
    "flash.pw_rules": {
        "en": "Password still needs: {rules}.",
        "ar": "باقي لكلمة السر: {rules}.",
    },
    "flash.pw_mismatch": {
        "en": "The two passwords don’t line up",
        "ar": "السِرين مو نفس السطر",
    },
    "flash.user_taken": {"en": "That name’s already in use", "ar": "الاسم موجود من قبل"},
    "flash.email_taken": {"en": "We already have that email", "ar": "هالإيميل مسجّل عندنا"},
    "pw.err.len": {"en": "8+ characters", "ar": "٨ أحرف فما فوق"},
    "pw.err.upper": {"en": "a cap letter", "ar": "حرف كبير"},
    "pw.err.digit": {"en": "a number", "ar": "رقم"},
    "pw.err.special": {"en": "a symbol", "ar": "رمز"},
    # ─── Status / Categories ─────────────────────────────────
    "cat.study": {"en": "Study", "ar": "دراسة"},
    "cat.work": {"en": "Work", "ar": "شغل"},
    "cat.personal": {"en": "Personal", "ar": "شخصي"},
    "status.pending": {"en": "pending", "ar": "بانتظارك"},
    "status.active": {"en": "active", "ar": "شغّال عليها"},
    "status.completed": {"en": "completed", "ar": "خلصت"},
    # ─── JS ─────────────────────────────────────────────────
    "js.load_fail": {"en": "Couldn’t load your list: ", "ar": "ما قدرت أجيب المهام: "},
    "js.task_added": {"en": "It’s on the list", "ar": "انضافت للمهمات ✔"},
    "js.error_prefix": {"en": "Hmm: ", "ar": "شي غلط: "},
    "js.delete_confirm": {"en": "Remove this one?", "ar": "أكيد تبي تحذفها؟"},
    "js.task_deleted": {"en": "Removed", "ar": "انشالت"},
    "js.tracking_started": {"en": "Timer’s running", "ar": "الوقت يمشي"},
    "js.task_done": {"en": "You closed it. Nice", "ar": "خلصتها 👏"},
    "js.no_match_filters": {
        "en": "Nothing here with those filters. Loosen one",
        "ar": "فاضي بهالفلتر. جرّب توسّع شوي",
    },
    "js.start": {"en": "Start", "ar": "شغّل"},
    "js.stop": {"en": "Stop", "ar": "قف"},
    "js.done": {"en": "Done", "ar": "ضبط"},
    "js.delete_title": {"en": "Delete", "ar": "حذف"},
    "js.min": {"en": "min", "ar": "د"},
    "js.min_suffix": {"en": " min", "ar": " د"},
    "focus.notify_pomo_title": {"en": "Round done 🎉", "ar": "خلصت الجلسة 🎉"},
    "focus.notify_pomo_body": {
        "en": "Stretch, drink water, breathe",
        "ar": "قم تحرك شوي وخذ لك بريك",
    },
    "focus.toast_pomo_done": {
        "en": "Block done. Step away for a bit",
        "ar": "خلصت الجلسة. رِحت لحظة",
    },
    "focus.notify_break_title": {"en": "Break is up", "ar": "خلصت الراحة"},
    "focus.notify_break_body": {"en": "Time to focus again", "ar": "يلا نرجع نركز"},
    "focus.toast_break_done": {
        "en": "Back in when you’re ready",
        "ar": "نكمّل لما تجهز",
    },
    "dash.load_rec_fail": {"en": "Couldn’t load those tips", "ar": "ما وصلت الاقتراحات"},
    "dash.unlock_insights": {
        "en": "Finish a few tasks and your insights will show up here.",
        "ar": "أكمل شوية مهام ويظهر لك هنا وضعك أوضح",
    },
    "dash.pred_title": {
        "en": "Tomorrow ({day}): your sweet spot looks like {range}",
        "ar": "بكرة ({day}): أحسن ساعة تقريبًا {range}",
    },
    "dash.pred_sub": {
        "en": "From your past weeks, {day}s usually feel best in that window",
        "ar": "من اللي تسجّل، نفس الوقت غالب يضبطك يوم {day}",
    },
    "dash.pred_confidence": {"en": "How sure we are", "ar": "قد إيه واثقين"},
    "dash.sessions_word": {"en": "earlier runs", "ar": "جلسات قبل"},
    "dash.fmt_min": {"en": "0 min", "ar": "٠ د"},
    "dash.fmt_sec": {"en": "s", "ar": "ث"},
    "dash.fmt_h": {"en": "h", "ar": "س"},
    "dash.breakdown_pts": {"en": "pts", "ar": "نقطة"},
    # ─── Analysis / API dynamic strings ─────────────────────
    "score.excellent": {"en": "On fire", "ar": "فُل 🔥"},
    "score.good": {"en": "Solid", "ar": "تمام"},
    "score.fair": {"en": "Room to grow", "ar": "يمديك أفضل"},
    "score.needs_work": {"en": "Let’s nudge it up", "ar": "شد حيلك شوي"},
    "conf.high": {"en": "High", "ar": "عالية"},
    "conf.medium": {"en": "Medium", "ar": "متوسطة"},
    "conf.low": {"en": "Low", "ar": "خفيفة"},
    # ─── Days ───────────────────────────────────────────────
    "dow.mon": {"en": "Monday", "ar": "الإثنين"},
    "dow.tue": {"en": "Tuesday", "ar": "الثلاثاء"},
    "dow.wed": {"en": "Wednesday", "ar": "الأربعاء"},
    "dow.thu": {"en": "Thursday", "ar": "الخميس"},
    "dow.fri": {"en": "Friday", "ar": "الجمعة"},
    "dow.sat": {"en": "Saturday", "ar": "السبت"},
    "dow.sun": {"en": "Sunday", "ar": "الأحد"},
    # ─── Warnings ───────────────────────────────────────────
    "warn.no_sessions": {
        "en": "You haven’t logged a focus block yet.",
        "ar": "للحين ما بدأت جلسة تركيز 👀",
    },
    "warn.none_today": {
        "en": "Today’s still quiet. Pop open Tasks and run one timer",
        "ar": "اليوم هادي شوي… افتح مهمة وابدأ مؤقت.",
    },
    "warn.low_today": {
        "en": "Only {m} min on the board today.",
        "ar": "اليوم ما أخذت إلا {m} دقيقة. تقدر تسوي أكثر 💪",
    },
    "warn.below_avg": {
        "en": "You’re at {t} min today.",
        "ar": "اليوم أنت على {t} دقيقة، وعادتك أعلى من كذا شوي.",
    },
    "warn.one_cat": {
        "en": "This week is all {c}.",
        "ar": "هالأسبوع كله {c} 👀 جرّب تغيّر شوي.",
    },
    # ─── Recommendations ────────────────────────────────────
    "rec.get_started_title": {"en": "First steps", "ar": "خلّنا نبدأ"},
    "rec.get_started_text": {
        "en": "Tick a few tasks and we can talk about you.",
        "ar": "خلص كم مهمة وبنبدأ نفهم نظامك أكثر.",
    },
    "rec.need_data_title": {"en": "We need a bit more", "ar": "نبغى معلومات أكثر شوي"},
    "rec.need_data_text": {
        "en": "Two done tasks and the tips get personal",
        "ar": "بس مهمتين زيادة وتصير الاقتراحات أذكى.",
    },
    "rec.peak_title": {"en": "When you’re strongest", "ar": "أفضل وقت لك"},
    "rec.peak_text": {
        "en": "You hit your peak at {h}",
        "ar": "غالبًا تركيزك يكون قوي حول {h}",
    },
    "rec.distraction_title": {"en": "Soft hour", "ar": "وقت تركيزك يخف"},
    "rec.distraction_text": {
        "en": "{h} is a rough spot for you",
        "ar": "عادة حول {h} تركيزك يخف شوي.",
    },
    "rec.short_sess_title": {"en": "Short bursts", "ar": "جلساتك قصيرة"},
    "rec.short_sess_text": {
        "en": "Averages are around {m} min.",
        "ar": "متوسط جلساتك {m} دقيقة. جرّب تطوّلها شوي.",
    },
    "rec.breaks_title": {"en": "Breathe on purpose", "ar": "خذ لك بريك"},
    "rec.breaks_text": {
        "en": "You’re holding long blocks.",
        "ar": "قاعد تطوّل كثير بالجلسات… خذ راحة بسيطة.",
    },
    "rec.sess_len_title": {"en": "How long you sit", "ar": "مدة جلساتك"},
    "rec.sess_len_text": {
        "en": "You’re landing near {m} min a run.",
        "ar": "غالبًا جلساتك حول {m} دقيقة، وهذا ممتاز.",
    },
    "rec.study_warn_title": {"en": "Study mix", "ar": "الدراسة عندك"},
    "rec.study_warn_text": {
        "en": "Only {p}% of time is study.",
        "ar": "الدراسة تمثل {p}% من وقتك الحالي.",
    },
    "rec.study_ok_title": {"en": "Study mix", "ar": "الدراسة عندك"},
    "rec.study_ok_text": {
        "en": "Nice, {p}% of your time is study.",
        "ar": "ممتاز 👏 الدراسة عندك تمثل {p}% من وقتك.",
    },
    "rec.streak_title": {"en": "Day streak", "ar": "استمراريتك"},
    "rec.streak_text": {
        "en": "You’ve chained {n} days in a row.",
        "ar": "لك {n} يوم مستمر 👏",
    },
    "rec.best_day_title": {"en": "Your power day", "ar": "يومك القوي"},
    "rec.best_day_text": {
        "en": "{day} keeps showing up strong.",
        "ar": "{day} غالبًا يكون أفضل يوم إنتاجية عندك.",
    },
    # ─── Prediction UI ──────────────────────────────────────
    "pred.ui_title": {
        "en": "Green light window for tomorrow ({day})",
        "ar": "أفضل وقت لك بكرة ({day})",
    },
    "pred.ui_sub": {
        "en": "Your past self usually likes that stretch",
        "ar": "حسب جلساتك السابقة، هذا الوقت غالبًا يناسبك.",
    },
    "pred.conf_line": {
        "en": "How sure: {c}",
        "ar": "مستوى الثقة: {c}",
    },
}

_DOW_KEYS = (
    "dow.mon",
    "dow.tue",
    "dow.wed",
    "dow.thu",
    "dow.fri",
    "dow.sat",
    "dow.sun",
)


def dow_name(i: int, locale: str | None = None) -> str:
    loc = locale if locale in LOCALES else get_locale()
    return tr(_DOW_KEYS[i % 7], loc)


def format_daily_chart_label(d, locale: str | None = None) -> str:
    """Format a date label for the daily chart."""
    loc = locale if locale in LOCALES else get_locale()

    if loc == "ar":
        ar_days = [
            "الإثنين",
            "الثلاثاء",
            "الأربعاء",
            "الخميس",
            "الجمعة",
            "السبت",
            "الأحد",
        ]
        return f"{ar_days[d.weekday()]} {d.day}"

    return d.strftime("%a %d")


def format_hour(hour: int, locale: str | None = None) -> str:
    """Format 0–23 as 12-hour clock (1–12) with AM/PM or ص/م."""
    loc = locale if locale in LOCALES else get_locale()
    h12 = hour % 12 or 12
    if loc == "ar":
        period = "ص" if hour < 12 else "م"
        return f"{h12} {period}"
    period = "AM" if hour < 12 else "PM"
    return f"{h12} {period}"


def format_hour_range(start_hour: int, end_hour: int, locale: str | None = None) -> str:
    """Format a time range; end_hour is the next hour tick (exclusive)."""
    loc = locale if locale in LOCALES else get_locale()
    return f"{format_hour(start_hour, loc)} – {format_hour(end_hour % 24, loc)}"


def get_locale() -> str:
    try:
        from flask import has_request_context, request

        if has_request_context() and request:
            loc = request.cookies.get(COOKIE_NAME, "en")
            return loc if loc in LOCALES else "en"

    except RuntimeError:
        pass

    return "en"


def tr(key: str, locale: str | None = None, **kwargs: Any) -> str:
    if locale is None:
        locale = get_locale()

    elif locale not in LOCALES:
        locale = "en"

    row = _MSG.get(key)

    if not row:
        return key

    text = row.get(locale) or row.get("en") or key

    if kwargs:
        try:
            return text.format(**kwargs)

        except (KeyError, ValueError):
            return text

    return text


def category_label(cat: str, locale: str | None = None) -> str:
    loc = locale or get_locale()

    m = {
        "Study": "cat.study",
        "Work": "cat.work",
        "Personal": "cat.personal",
    }

    return tr(m.get(cat, "cat.study"), loc)


def status_label(status: str, locale: str | None = None) -> str:
    loc = locale or get_locale()

    m = {
        "pending": "status.pending",
        "active": "status.active",
        "completed": "status.completed",
    }

    return tr(m.get(status, status), loc)


def js_bundle(locale: str | None = None) -> dict[str, str]:
    """Strings needed by JS files."""
    loc = locale if locale in LOCALES else get_locale()

    keys = [
        "tasks.filter_all",
        "tasks.filter_pending",
        "tasks.filter_active",
        "tasks.filter_completed",
        "tasks.filter_cat_all",
        "tasks.empty",
        "cat.study",
        "cat.work",
        "cat.personal",
        "status.pending",
        "status.active",
        "status.completed",
        "js.load_fail",
        "js.task_added",
        "js.error_prefix",
        "js.delete_confirm",
        "js.task_deleted",
        "js.tracking_started",
        "js.task_done",
        "js.no_match_filters",
        "js.start",
        "js.stop",
        "js.done",
        "js.delete_title",
        "js.min",
        "js.min_suffix",
        "focus.duration_label",
        "focus.duration_unit",
        "focus.label_focus",
        "focus.label_short",
        "focus.label_long",
        "focus.start",
        "focus.resume",
        "focus.notify_pomo_title",
        "focus.notify_pomo_body",
        "focus.toast_pomo_done",
        "focus.notify_break_title",
        "focus.notify_break_body",
        "focus.toast_break_done",
        "focus.doc_title",
        "focus.title_flash",
        "dash.load_rec_fail",
        "dash.unlock_insights",
        "dash.chart_minutes",
        "dash.no_cat_data",
        "dash.pred_title",
        "dash.pred_sub",
        "dash.pred_confidence",
        "dash.sessions_word",
        "dash.fmt_min",
        "dash.fmt_sec",
        "dash.fmt_h",
        "dash.breakdown_pts",
        "auth.pw_weak",
        "auth.pw_fair",
        "auth.pw_good",
        "auth.pw_strong",
        "auth.pw_match_ok",
        "auth.pw_match_bad",
    ]

    return {
        k.replace(".", "_"): tr(k, loc)
        for k in keys
    }


def template_globals() -> dict[str, Any]:
    loc = get_locale()

    return {
        "locale": loc,
        "is_rtl": loc == "ar",
        "t": lambda key, **kw: tr(key, loc, **kw),
        "category_label": lambda c: category_label(c, loc),
        "status_label": lambda s: status_label(s, loc),
        "format_hour": lambda h: format_hour(h, loc),
        "format_hour_range": lambda s, e: format_hour_range(s, e, loc),
        "js_i18n": js_bundle(loc),
    }
