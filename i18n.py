"""English / Arabic translations for Wagti."""

from __future__ import annotations

from typing import Any

LOCALES = frozenset({"en", "ar"})
COOKIE_NAME = "sf_locale"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365

# Flat keys: en / ar string values. Use {name} placeholders where needed.
_MSG: dict[str, dict[str, str]] = {
    # ─── Nav / chrome ─────────────────────────────────────────────────────────
    "brand.tagline": {
        "en": "Track. Focus. Improve.",
        "ar": "تتبّع. ركّز. تحسّن.",
    },
    "nav.tasks": {"en": "Tasks", "ar": "المهام"},
    "nav.focus": {"en": "Focus", "ar": "التركيز"},
    "nav.insights": {"en": "Insights", "ar": "الرؤى"},
    "nav.guest": {"en": "Guest", "ar": "زائر"},
    "nav.signup_title": {"en": "Create a free account", "ar": "إنشاء حساب مجاني"},
    "nav.logout_title": {"en": "Sign out", "ar": "تسجيل الخروج"},
    "nav.theme_title": {"en": "Switch theme", "ar": "تبديل المظهر"},
    "nav.menu_aria": {"en": "Menu", "ar": "القائمة"},
    "nav.lang_switch_en": {"en": "English", "ar": "English"},
    "nav.lang_switch_ar": {"en": "العربية", "ar": "العربية"},
    "guest.banner": {
        "en": 'You are using a <strong>guest session</strong> — your data is temporary.',
        "ar": "أنت تستخدم <strong>جلسة زائر</strong> — بياناتك مؤقتة.",
    },
    "guest.banner_link": {"en": "Create a free account", "ar": "إنشاء حساب مجاني"},
    "guest.banner_suffix": {"en": "to save it permanently.", "ar": "لحفظها بشكل دائم."},
    "footer.tagline": {"en": "Stay productive, stay focused.", "ar": "كن منتجًا، كن مركزًا."},
    # ─── Landing ───────────────────────────────────────────────────────────────
    "landing.title": {"en": "Wagti | Smart Focus & Productivity Tracker", "ar": "وقتي | لتتبع التركيز والإنتاجية"},
    "landing.badge": {"en": "Smart Focus System", "ar": "نظام تركيز ذكي"},
    "landing.hero_l1": {"en": "Own your time.", "ar": "امتلك وقتك."},
    "landing.hero_l2": {"en": "Improve your focus.", "ar": "حسّن تركيزك."},
    "landing.sub": {
        "en": "Wagti helps you track tasks, build deep focus habits with Pomodoro, and get smart insights on your productivity — all in one place.",
        "ar": "يساعدك وقتي على تتبّع المهام، وبناء عادات تركيز عميق مع بومودورو، والحصول على رؤى ذكية حول إنتاجيتك — كل ذلك في مكان واحد.",
    },
    "landing.based_on": {"en": "Based on your real behavior — not guesses.", "ar": "بناءً على سلوكك الحقيقي — لا  بحسب التخمين."},
    "landing.cta_register": {"en": "Get Started Free", "ar": "ابدأ مجانًا"},
    "landing.cta_guest": {"en": "Try as Guest", "ar": "جرّب كزائر"},
    "landing.note": {"en": "Already have an account?", "ar": "لديك حساب بالفعل؟"},
    "landing.sign_in": {"en": "Sign in", "ar": "تسجيل الدخول"},
    "landing.hero_focus_score": {"en": "Focus Score", "ar": "درجة التركيز"},
    "landing.hero_good": {"en": "Good", "ar": "جيد"},
    "landing.hero_warning": {
        "en": "Low focus today (12 min). Start a 25-min session to improve.",
        "ar": "تركيز منخفض اليوم (١٢ د). ابدأ جلسة ٢٥ دقيقة للتحسين.",
    },
    "landing.hero_ai": {"en": "AI Prediction", "ar": "توقع ذكي"},
    "landing.hero_ai_text": {
        "en": "Learns your habits and predicts your best focus time. Best window:",
        "ar": "يتعلّم عاداتك ويتوقّع أفضل وقت تركيز. أفضل نافذة:",
    },
    "landing.features_title": {"en": "Everything you need to stay focused", "ar": "كل ما تحتاجه للبقاء مركزًا"},
    "landing.f1_title": {"en": "Manage Your Time", "ar": "أدِر وقتك"},
    "landing.f1_text": {
        "en": "Add tasks, set time goals, and track exactly how long each one takes.",
        "ar": "أضِف مهامًا، حدّد أهدافًا زمنية، وتتبّع مدة كل مهمة بدقة.",
    },
    "landing.f2_title": {"en": "Deep Focus Timer", "ar": "مؤقّت تركيز عميق"},
    "landing.f2_text": {
        "en": "Built-in Pomodoro timer with short and long breaks. Alerts you if you switch tabs.",
        "ar": "مؤقّت بومودورو مع فترات راحة قصيرة وطويلة. ينبّهك عند تبديل الصفحات.",
    },
    "landing.f3_title": {"en": "Insights Dashboard", "ar": "لوحة الرؤى"},
    "landing.f3_text": {
        "en": "Visual charts for daily focus, category breakdown, and hourly productivity patterns.",
        "ar": "مخططات للتركيز اليومي، التوزيع حسب الفئة، وأنماط الإنتاجية بالساعة.",
    },
    "landing.f4_title": {"en": "Focus Score", "ar": "درجة التركيز"},
    "landing.f4_text": {
        "en": "A 0–100 score based on your focus time, tasks completed, and consistency streak.",
        "ar": "درجة من ٠–١٠٠ تعتمد على وقت التركيز والمهام المنجزة واستمراريتك.",
    },
    "landing.f5_title": {"en": "Focus Alerts", "ar": "تنبيهات التركيز"},
    "landing.f5_text": {
        "en": "Smart warnings when your focus drops below your daily average.",
        "ar": "تحذيرات ذكية عندما يقل تركيزك عن متوسطك اليومي.",
    },
    "landing.f6_title": {"en": "AI Prediction", "ar": "توقع ذكي"},
    "landing.f6_text": {
        "en": "Analyzes your past sessions to recommend your most productive hours.",
        "ar": "يحلّل جلساتك السابقة ليقترح أكثر ساعاتك إنتاجية.",
    },
    "landing.final_title": {"en": "Take control of your time today.", "ar": "تحكّم في وقتك اليوم."},
    "landing.final_sub": {"en": "Free forever. No credit card. Start in seconds.", "ar": "مجاني .. ابدأ في ثوانٍ."},
    "landing.cta_create": {"en": "Create Free Account", "ar": "إنشاء حساب مجاني"},
    "landing.final_note": {"en": "No distractions. No complexity. Just focus.", "ar": "لا إلهاء. لا تعقيد. تركيز فقط."},
    # ─── Tasks page ────────────────────────────────────────────────────────────
    "tasks.title_page": {"en": "Tasks — Wagti", "ar": "المهام — وقتي"},
    "tasks.header": {"en": "Manage Your Time", "ar": "أدِر وقتك"},
    "tasks.sub": {"en": "Add tasks, set goals, and track your time.", "ar": "أضِف مهامًا، حدّد أهدافًا، وتتبّع وقتك."},
    "tasks.new_task": {"en": "New Task", "ar": "مهمة جديدة"},
    "tasks.task_name": {"en": "Task Name", "ar": "اسم المهمة"},
    "tasks.placeholder_name": {"en": "e.g. Study Chapter 3", "ar": "مثال: مراجعة الفصل ٣"},
    "tasks.category": {"en": "Category", "ar": "الفئة"},
    "tasks.goal_min": {"en": "Goal (minutes)", "ar": "الهدف (دقائق)"},
    "tasks.add": {"en": "Add Task", "ar": "إضافة مهمة"},
    "tasks.stat_active": {"en": "Active Tasks", "ar": "مهام نشطة"},
    "tasks.stat_completed": {"en": "Completed Today", "ar": "مكتمل اليوم"},
    "tasks.stat_time": {"en": "Total Time Today", "ar": "الوقت الكلي اليوم"},
    "tasks.your_tasks": {"en": "Your Tasks", "ar": "مهامك"},
    "tasks.filter_all": {"en": "All", "ar": "الكل"},
    "tasks.filter_pending": {"en": "Pending", "ar": "معلّقة"},
    "tasks.filter_active": {"en": "Active", "ar": "نشطة"},
    "tasks.filter_completed": {"en": "Completed", "ar": "مكتملة"},
    "tasks.filter_cat_all": {"en": "All Categories", "ar": "كل الفئات"},
    "tasks.empty": {"en": "No tasks yet. Add one above to get started!", "ar": "لا مهام بعد. أضِف واحدة أعلاه للبدء!"},
    "cat.study": {"en": "Study", "ar": "دراسة"},
    "cat.work": {"en": "Work", "ar": "عمل"},
    "cat.personal": {"en": "Personal", "ar": "شخصي"},
    "status.pending": {"en": "pending", "ar": "معلّقة"},
    "status.active": {"en": "active", "ar": "نشطة"},
    "status.completed": {"en": "completed", "ar": "مكتملة"},
    # ─── Focus page ────────────────────────────────────────────────────────────
    "focus.title_page": {"en": "Deep Focus — Wagti", "ar": "تركيز عميق — وقتي"},
    "focus.header": {"en": "Deep Focus", "ar": "تركيز عميق"},
    "focus.sub": {
        "en": "Use the Pomodoro technique to stay focused and productive.",
        "ar": "استخدم تقنية بومودورو للبقاء مركزًا ومنتجًا.",
    },
    "focus.mode_pom": {"en": "Pomodoro (25 min)", "ar": "بومودورو (٢٥ د)"},
    "focus.mode_short": {"en": "Short Break (5 min)", "ar": "راحة قصيرة (٥ د)"},
    "focus.mode_long": {"en": "Long Break (15 min)", "ar": "راحة طويلة (١٥ د)"},
    "focus.label_focus": {"en": "Focus", "ar": "تركيز"},
    "focus.label_short": {"en": "Short Break", "ar": "راحة قصيرة"},
    "focus.label_long": {"en": "Long Break", "ar": "راحة طويلة"},
    "focus.start": {"en": "Start", "ar": "ابدأ"},
    "focus.pause": {"en": "Pause", "ar": "إيقاف مؤقت"},
    "focus.resume": {"en": "Resume", "ar": "استئناف"},
    "focus.reset": {"en": "Reset", "ar": "إعادة"},
    "focus.sound_alerts": {"en": "Sound alerts when timer ends", "ar": "تنبيه صوتي عند انتهاء المؤقت"},
    "focus.alert": {"en": "You left the focus session! Stay on track.", "ar": "غادرت جلسة التركيز! التزم بالمسار."},
    "focus.tips_title": {"en": "Pomodoro Technique", "ar": "تقنية بومودورو"},
    "focus.tip1": {"en": "Work for", "ar": "اعمل لمدة"},
    "focus.tip1b": {"en": "25 minutes", "ar": "٢٥ دقيقة"},
    "focus.tip1c": {"en": "without distraction", "ar": "دون انقطاع"},
    "focus.tip2": {"en": "Take a", "ar": "خُذ"},
    "focus.tip2b": {"en": "5-minute", "ar": "٥ دقائق"},
    "focus.tip2c": {"en": "short break", "ar": "راحة قصيرة"},
    "focus.tip3": {"en": "Repeat 4 times, then take a", "ar": "كرّر ٤ مرات، ثم خُذ"},
    "focus.tip3b": {"en": "15-minute", "ar": "١٥ دقيقة"},
    "focus.tip3c": {"en": "long break", "ar": "راحة طويلة"},
    "focus.tip4": {"en": "Each full cycle = 1 Pomodoro set", "ar": "كل دورة كاملة = مجموعة بومودورو واحدة"},
    "focus.stats_title": {"en": "Session Stats", "ar": "إحصاءات الجلسة"},
    "focus.pom_today": {"en": "Pomodoros Today", "ar": "بومودورو اليوم"},
    "focus.total_focus": {"en": "Total Focus Time", "ar": "وقت التركيز الكلي"},
    "focus.current_mode": {"en": "Current Mode", "ar": "الوضع الحالي"},
    "focus.doc_title": {"en": "Deep Focus — Wagti", "ar": "تركيز عميق — وقتي"},
    "focus.title_flash": {"en": "⚠️ Stay Focused!", "ar": "⚠️ ابقَ مركزًا!"},
    # ─── Dashboard ───────────────────────────────────────────────────────────────
    "dash.title_page": {"en": "Insights — Wagti", "ar": "الرؤى — وقتي"},
    "dash.header": {"en": "Insights", "ar": "الرؤى"},
    "dash.sub": {
        "en": "Visualize your productivity patterns and track your progress.",
        "ar": "تصوّر أنماط إنتاجيتك وتتبّع تقدّمك.",
    },
    "dash.today_focus": {"en": "Today's Focus", "ar": "تركيز اليوم"},
    "dash.tasks_today": {"en": "Tasks Today", "ar": "مهام اليوم"},
    "dash.alltime": {"en": "All-Time Hours", "ar": "ساعات كلّ الوقت"},
    "dash.focus_score": {"en": "Focus Score", "ar": "درجة التركيز"},
    "dash.focus_alerts": {"en": "Focus Alerts", "ar": "تنبيهات التركيز"},
    "dash.chart_daily": {"en": "Daily Focus (Last 7 Days)", "ar": "التركيز اليومي (آخر ٧ أيام)"},
    "dash.chart_cat": {"en": "Today by Category", "ar": "اليوم حسب الفئة"},
    "dash.chart_hourly": {"en": "Hourly Productivity (All Time)", "ar": "الإنتاجية بالساعة (كلّ الوقت)"},
    "dash.no_cat_data": {"en": "No data for today yet.", "ar": "لا بيانات لهذا اليوم بعد."},
    "dash.ai_pred": {"en": "AI Prediction", "ar": "توقع ذكي"},
    "dash.rec_title": {"en": "Insights & Suggestions", "ar": "رؤى واقتراحات"},
    "dash.loading_rec": {"en": "Loading recommendations...", "ar": "جاري تحميل التوصيات..."},
    "dash.breakdown": {"en": "Performance Breakdown", "ar": "تفصيل الأداء"},
    "dash.br_focus": {"en": "Focus Time", "ar": "وقت التركيز"},
    "dash.br_tasks": {"en": "Tasks Completed", "ar": "مهام مكتملة"},
    "dash.br_cons": {"en": "Consistency (7 days)", "ar": "الاستمرارية (٧ أيام)"},
    "dash.chart_minutes": {"en": "Minutes", "ar": "دقائق"},
    "dash.pts": {"en": "pts", "ar": "نقطة"},
    # ─── Auth ───────────────────────────────────────────────────────────────────
    "auth.back_title": {"en": "Back to home", "ar": "العودة للرئيسية"},
    "auth.register_title": {"en": "Register — Wagti", "ar": "تسجيل — وقتي"},
    "auth.login_title": {"en": "Login — Wagti", "ar": "دخول — وقتي"},
    "auth.create_title": {"en": "Create your account", "ar": "أنشئ حسابك"},
    "auth.create_sub": {"en": "Create your account and start focusing in seconds.", "ar": "أنشئ حسابك وابدأ التركيز في ثوانٍ."},
    "auth.welcome": {"en": "Welcome back", "ar": "مرحبًا بعودتك"},
    "auth.signin_sub": {"en": "Sign in to your account", "ar": "سجّل الدخول إلى حسابك"},
    "auth.username": {"en": "Username", "ar": "اسم المستخدم"},
    "auth.ph_user": {"en": "Enter your username", "ar": "أدخل اسم المستخدم"},
    "auth.email": {"en": "Email", "ar": "البريد الإلكتروني"},
    "auth.ph_email": {"en": "you@example.com", "ar": "you@example.com"},
    "auth.password": {"en": "Password", "ar": "كلمة المرور"},
    "auth.ph_password": {"en": "Enter your password", "ar": "أدخل كلمة المرور"},
    "auth.ph_create_pw": {"en": "Create a strong password", "ar": "أنشئ كلمة مرور قوية"},
    "auth.confirm": {"en": "Confirm Password", "ar": "تأكيد كلمة المرور"},
    "auth.ph_confirm": {"en": "Repeat your password", "ar": "كرّر كلمة المرور"},
    "auth.req_len": {"en": "At least 8 characters", "ar": "٨ أحرف على الأقل"},
    "auth.req_upper": {"en": "One uppercase letter (A–Z)", "ar": "حرف كبير واحد (A–Z)"},
    "auth.req_digit": {"en": "One number (0–9)", "ar": "رقم واحد (٠–٩)"},
    "auth.req_special": {"en": "One special character (!@#$...)", "ar": "رمز خاص واحد (!@#$...)"},
    "auth.sign_in": {"en": "Sign In", "ar": "تسجيل الدخول"},
    "auth.create_account": {"en": "Create Account", "ar": "إنشاء حساب"},
    "auth.or": {"en": "or", "ar": "أو"},
    "auth.guest": {"en": "Continue as Guest", "ar": "المتابعة كزائر"},
    "auth.have_account": {"en": "Already have an account?", "ar": "لديك حساب بالفعل؟"},
    "auth.sign_in_link": {"en": "Sign in", "ar": "تسجيل الدخول"},
    "auth.no_account": {"en": "Don't have an account?", "ar": "ليس لديك حساب؟"},
    "auth.create_free": {"en": "Create one free", "ar": "أنشئ حسابًا مجانيًا"},
    "auth.pw_weak": {"en": "Weak", "ar": "ضعيف"},
    "auth.pw_fair": {"en": "Fair", "ar": "مقبول"},
    "auth.pw_good": {"en": "Good", "ar": "جيد"},
    "auth.pw_strong": {"en": "Strong", "ar": "قوي"},
    "auth.pw_match_ok": {"en": "✓ Passwords match", "ar": "✓ كلمتا المرور متطابقتان"},
    "auth.pw_match_bad": {"en": "✗ Passwords do not match", "ar": "✗ كلمتا المرور غير متطابقتين"},
    # API / flash (app.py)
    "api.task_name_required": {"en": "task_name is required", "ar": "اسم المهمة مطلوب"},
    "api.task_deleted": {"en": "Task deleted", "ar": "تم حذف المهمة"},
    "api.task_completed": {"en": "Task already completed", "ar": "المهمة مكتملة بالفعل"},
    "api.task_not_active": {"en": "Task is not active", "ar": "المهمة غير نشطة"},
    "flash.login_bad": {"en": "Incorrect username or password.", "ar": "اسم المستخدم أو كلمة المرور غير صحيحة."},
    "flash.all_required": {"en": "All fields are required.", "ar": "جميع الحقول مطلوبة."},
    "flash.pw_rules": {"en": "Password must contain: {rules}.", "ar": "يجب أن تحتوي كلمة المرور على: {rules}."},
    "flash.pw_mismatch": {"en": "Passwords do not match.", "ar": "كلمتا المرور غير متطابقتين."},
    "flash.user_taken": {"en": "Username already taken.", "ar": "اسم المستخدم مستخدم بالفعل."},
    "flash.email_taken": {"en": "Email already registered.", "ar": "البريد الإلكتروني مسجّل بالفعل."},
    "pw.err.len": {"en": "at least 8 characters", "ar": "٨ أحرف على الأقل"},
    "pw.err.upper": {"en": "one uppercase letter", "ar": "حرف كبير واحد"},
    "pw.err.digit": {"en": "one number", "ar": "رقم واحد"},
    "pw.err.special": {"en": "one special character", "ar": "رمز خاص واحد"},
    # ─── JS-only (also used by js_bundle) ─────────────────────────────────────
    "js.load_fail": {"en": "Failed to load tasks: ", "ar": "تعذّر تحميل المهام: "},
    "js.task_added": {"en": "Task added!", "ar": "تمت إضافة المهمة!"},
    "js.error_prefix": {"en": "Error: ", "ar": "خطأ: "},
    "js.delete_confirm": {"en": "Delete this task?", "ar": "حذف هذه المهمة؟"},
    "js.task_deleted": {"en": "Task deleted", "ar": "تم حذف المهمة"},
    "js.tracking_started": {"en": "Tracking started!", "ar": "بدأ التتبّع!"},
    "js.task_done": {"en": "Task completed! Great work.", "ar": "اكتملت المهمة! أحسنت."},
    "js.no_match_filters": {"en": "No tasks match your filters.", "ar": "لا مهام تطابق المرشّحات."},
    "js.start": {"en": "Start", "ar": "ابدأ"},
    "js.stop": {"en": "Stop", "ar": "إيقاف"},
    "js.done": {"en": "Done", "ar": "تم"},
    "js.delete_title": {"en": "Delete", "ar": "حذف"},
    "js.min": {"en": "min", "ar": "د"},
    "js.min_suffix": {"en": " min", "ar": " د"},
    "focus.notify_pomo_title": {"en": "Pomodoro Complete! 🎉", "ar": "اكتمل البومودورو! 🎉"},
    "focus.notify_pomo_body": {"en": "Great work! Time for a break.", "ar": "أحسنت! حان وقت الراحة."},
    "focus.toast_pomo_done": {"en": "Pomodoro done! Take a break.", "ar": "انتهى البومودورو! خُذ راحة."},
    "focus.notify_break_title": {"en": "Break Over!", "ar": "انتهت الراحة!"},
    "focus.notify_break_body": {"en": "Time to focus again.", "ar": "حان وقت التركيز مجددًا."},
    "focus.toast_break_done": {
        "en": "Break finished. Let's get back to work!",
        "ar": "انتهت الراحة. لنعُد للعمل!",
    },
    "dash.load_rec_fail": {"en": "Could not load recommendations.", "ar": "تعذّر تحميل التوصيات."},
    "dash.unlock_insights": {
        "en": "Complete more tasks to unlock insights.",
        "ar": "أكمل المزيد من المهام لفتح الرؤى.",
    },
    "dash.pred_title": {
        "en": "Tomorrow ({day}): Best focus at {range}",
        "ar": "غدًا ({day}): أفضل تركيز عند {range}",
    },
    "dash.pred_sub": {
        "en": "Based on your historical patterns, you are most productive during this window on {day}s.",
        "ar": "بناءً على أنماطك السابقة، أنت أكثر إنتاجية خلال هذه النافذة أيام {day}.",
    },
    "dash.pred_confidence": {"en": "Confidence:", "ar": "الثقة:"},
    "dash.sessions_word": {"en": "past sessions", "ar": "جلسات سابقة"},
    "dash.fmt_min": {"en": "0 min", "ar": "٠ د"},
    "dash.fmt_sec": {"en": "s", "ar": "ث"},
    "dash.fmt_h": {"en": "h", "ar": "س"},
    "dash.breakdown_pts": {"en": "pts", "ar": "نقطة"},
    # ─── Analysis / API dynamic strings ────────────────────────────────────────
    "score.excellent": {"en": "Excellent", "ar": "ممتاز"},
    "score.good": {"en": "Good", "ar": "جيد"},
    "score.fair": {"en": "Fair", "ar": "مقبول"},
    "score.needs_work": {"en": "Needs work", "ar": "يحتاج تحسين"},
    "conf.high": {"en": "High", "ar": "عالية"},
    "conf.medium": {"en": "Medium", "ar": "متوسطة"},
    "conf.low": {"en": "Low", "ar": "منخفضة"},
    "dow.mon": {"en": "Monday", "ar": "الاثنين"},
    "dow.tue": {"en": "Tuesday", "ar": "الثلاثاء"},
    "dow.wed": {"en": "Wednesday", "ar": "الأربعاء"},
    "dow.thu": {"en": "Thursday", "ar": "الخميس"},
    "dow.fri": {"en": "Friday", "ar": "الجمعة"},
    "dow.sat": {"en": "Saturday", "ar": "السبت"},
    "dow.sun": {"en": "Sunday", "ar": "الأحد"},
    "warn.no_sessions": {
        "en": "No focus sessions completed yet. Start your first task to begin tracking!",
        "ar": "لم تُكمل أي جلسة تركيز بعد. ابدأ مهمتك الأولى لتفعيل التتبّع!",
    },
    "warn.none_today": {
        "en": "No focus sessions completed today. Open the Tasks page and start a task!",
        "ar": "لم تُكمل أي جلسة تركيز اليوم. افتح صفحة المهام وابدأ مهمة!",
    },
    "warn.low_today": {
        "en": "Low focus today ({m} min). Start a 25-min session to improve.",
        "ar": "تركيز منخفض اليوم ({m} د). ابدأ جلسة ٢٥ دقيقة للتحسين.",
    },
    "warn.below_avg": {
        "en": "Today's focus ({t} min) is well below your daily average ({a} min). You can do better!",
        "ar": "تركيز اليوم ({t} د) أقل بكثير من متوسطك اليومي ({a} د). يمكنك الأفضل!",
    },
    "warn.one_cat": {
        "en": "All your tasks this week are '{c}'. Add variety with Work or Personal tasks.",
        "ar": "كل مهامك هذا الأسبوع '{c}'. نوّع بمهام عمل أو شخصية.",
    },
    "rec.get_started_title": {"en": "Get Started", "ar": "ابدأ"},
    "rec.get_started_text": {
        "en": "Complete a few tasks to receive personalized recommendations.",
        "ar": "أكمل بعض المهام للحصول على توصيات مخصّصة.",
    },
    "rec.need_data_title": {"en": "Not Enough Data", "ar": "بيانات غير كافية"},
    "rec.need_data_text": {
        "en": "Complete at least 2 tasks to unlock smart recommendations.",
        "ar": "أكمل مهمتين على الأقل لفتح التوصيات الذكية.",
    },
    "rec.peak_title": {"en": "Peak Focus Hour", "ar": "ساعة الذروة"},
    "rec.peak_text": {
        "en": "Your peak focus hour is {h}:00 ({p} min total focused). Schedule your hardest tasks before {c}:00 for best results.",
        "ar": "ساعة ذروة تركيزك {h}:٠٠ ({p} د إجمالي). جدول أصعب مهامك قبل {c}:٠٠ لأفضل نتائج.",
    },
    "rec.distraction_title": {"en": "Distraction Alert", "ar": "تنبيه تشتيت"},
    "rec.distraction_text": {
        "en": "{h}:00 is your weakest hour (avg {a} min per session). Avoid scheduling deep work at this time.",
        "ar": "{h}:٠٠ هي أضعف ساعة لديك (متوسط {a} د لكل جلسة). تجنّب جدولة عمل عميق في هذا الوقت.",
    },
    "rec.short_sess_title": {"en": "Sessions Too Short", "ar": "جلسات قصيرة جدًا"},
    "rec.short_sess_text": {
        "en": "Your average session is only {m} min. Your sessions are too short — try completing full 25-min focus blocks.",
        "ar": "متوسط جلساتك {m} د فقط. الجلسات قصيرة جدًا — حاول إكمال كتل تركيز ٢٥ دقيقة.",
    },
    "rec.breaks_title": {"en": "Take Breaks", "ar": "خُذ فترات راحة"},
    "rec.breaks_text": {
        "en": "Your average session is {m} min — impressive! Remember to take 5-min breaks to avoid burnout.",
        "ar": "متوسط جلساتك {m} د — رائع! تذكّر أخذ راحات ٥ دقائق لتجنّب الإرهاق.",
    },
    "rec.sess_len_title": {"en": "Session Length", "ar": "طول الجلسة"},
    "rec.sess_len_text": {
        "en": "Your average focus session is {m} min. Keep building consistency!",
        "ar": "متوسط جلسة تركيزك {m} د. واصل بناء الاستمرارية!",
    },
    "rec.study_warn_title": {"en": "Study Balance", "ar": "توازن الدراسة"},
    "rec.study_warn_text": {
        "en": "Only {p}% of your tracked time is Study. Try to dedicate at least 40% of focus time to learning.",
        "ar": "فقط {p}% من وقتك المسجّل دراسة. حاول تخصيص ٤٠% على الأقل للتعلّم.",
    },
    "rec.study_ok_title": {"en": "Study Balance", "ar": "توازن الدراسة"},
    "rec.study_ok_text": {
        "en": "Great! {p}% of your total time is Study. Keep it up!",
        "ar": "رائع! {p}% من وقتك الكلي دراسة. واصل!",
    },
    "rec.streak_title": {"en": "Focus Streak", "ar": "سلسلة التركيز"},
    "rec.streak_text": {
        "en": "Your longest streak is {n} consecutive days. Consistency compounds — keep showing up daily!",
        "ar": "أطول سلسلة لك {n} أيام متتالية. الاستمرارية تتراكم — واظب يوميًا!",
    },
    "rec.best_day_title": {"en": "Best Day", "ar": "أفضل يوم"},
    "rec.best_day_text": {
        "en": "{day} is your most productive day ({m} min total). Plan your most important work for {day}s.",
        "ar": "{day} هو أكثر أيامك إنتاجية ({m} د إجمالي). خطّط لأهم عملك أيام {day}.",
    },
    "pred.ui_title": {
        "en": "Best focus window for tomorrow ({day})",
        "ar": "أفضل نافذة تركيز لغد ({day})",
    },
    "pred.ui_sub": {
        "en": "Historical pattern suggests this time range on {day}s.",
        "ar": "النمط التاريخي يقترح هذا النطاق الزمني أيام {day}.",
    },
    "pred.conf_line": {
        "en": "Confidence: {c} · {n} past sessions",
        "ar": "الثقة: {c} · {n} جلسات سابقة",
    },
}

_DOW_KEYS = ("dow.mon", "dow.tue", "dow.wed", "dow.thu", "dow.fri", "dow.sat", "dow.sun")


def dow_name(i: int, locale: str | None = None) -> str:
    loc = locale if locale in LOCALES else get_locale()
    return tr(_DOW_KEYS[i % 7], loc)


def format_daily_chart_label(d, locale: str | None = None) -> str:
    """Format a date label for the daily chart (last 7 days)."""
    loc = locale if locale in LOCALES else get_locale()
    if loc == "ar":
        ar_days = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
        return f"{ar_days[d.weekday()]} {d.day}"
    return d.strftime("%a %d")


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
    m = {"Study": "cat.study", "Work": "cat.work", "Personal": "cat.personal"}
    return tr(m.get(cat, "cat.study"), loc)


def status_label(status: str, locale: str | None = None) -> str:
    loc = locale or get_locale()
    m = {"pending": "status.pending", "active": "status.active", "completed": "status.completed"}
    return tr(m.get(status, status), loc)


def js_bundle(locale: str | None = None) -> dict[str, str]:
    """Strings needed by main.js, focus.js, dashboard.js."""
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
    return {k.replace(".", "_"): tr(k, loc) for k in keys}


def template_globals() -> dict[str, Any]:
    loc = get_locale()
    return {
        "locale": loc,
        "is_rtl": loc == "ar",
        "t": lambda key, **kw: tr(key, loc, **kw),
        "category_label": lambda c: category_label(c, loc),
        "status_label": lambda s: status_label(s, loc),
        "js_i18n": js_bundle(loc),
    }
