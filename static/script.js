// کدهای جاوااسکریپت تعاملی و کامل همراه با افکت‌ها و انیمیشن‌ها

function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    
    const targetTab = document.getElementById(tabId);
    if (targetTab) targetTab.classList.add('active');
    
    const activeBtn = document.getElementById('btn-' + tabId);
    if (activeBtn) activeBtn.classList.add('active');
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add('active');
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
}

// ورود کاربران با یوزرنیم و پسوورد
async function handleLogin(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    
    try {
        const response = await fetch('/login', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        
        if (result.success) {
            alert('ورود با موفقیت انجام شد!');
            window.location.reload();
        } else {
            alert(result.message);
        }
    } catch (err) {
        alert('خطا در ارتباط با سرور');
    }
}

// خرید بسته
let selectedPkgName = '';
function prepareBuy(pkgName) {
    selectedPkgName = pkgName;
    const userLoggedIn = document.body.getAttribute('data-user-logged') === 'true';
    if (!userLoggedIn) {
        openModal('login-modal');
    } else {
        document.getElementById('buy-pkg-title').innerText = 'خرید بسته: ' + pkgName;
        openModal('buy-modal');
    }
}

async function confirmBuy() {
    const formData = new FormData();
    formData.append('pkg_name', selectedPkgName);
    
    const res = await fetch('/api/buy', { method: 'POST', body: formData });
    const data = await res.json();
    alert(data.message);
    closeModal('buy-modal');
}

// ورود به پنل مدیریت با درخواست پسکد
async function checkAdminPass() {
    const passcode = prompt("رمز عبور مدیریت را وارد کنید:");
    if (!passcode) return;
    
    const formData = new FormData();
    formData.append('passcode', passcode);
    
    const res = await fetch('/api/admin_login', { method: 'POST', body: formData });
    const data = await res.json();
    
    if (data.success) {
        window.location.href = '/admin';
    } else {
        alert(data.message);
    }
}

// تغییر بخش‌های پنل مدیریت
function switchAdminSection(sectionId) {
    document.querySelectorAll('.admin-section').forEach(sec => sec.classList.remove('active'));
    document.querySelectorAll('.sidebar-btn').forEach(btn => btn.classList.remove('active'));
    
    const targetSection = document.getElementById('sec-' + sectionId);
    if (targetSection) targetSection.classList.add('active');
    
    const activeBtn = document.getElementById('sbtn-' + sectionId);
    if (activeBtn) activeBtn.classList.add('active');
}

// بروزرسانی زنده وضعیت سرور (CPU / RAM)
function updateCircleGauge(circleId, textId, percent, color) {
    const circle = document.getElementById(circleId);
    const text = document.getElementById(textId);
    if (!circle || !text) return;
    
    const circumference = 377;
    const offset = circumference - (percent / 100) * circumference;
    
    circle.style.strokeDashoffset = offset;
    circle.style.stroke = percent > 80 ? '#ef4444' : percent > 50 ? '#f59e0b' : color;
    text.innerText = percent.toFixed(1) + '%';
}

async function fetchStats() {
    try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        updateCircleGauge('cpu-gauge', 'cpu-text', data.cpu, '#38bdf8');
        updateCircleGauge('ram-gauge', 'ram-text', data.ram, '#a855f7');
    } catch (e) {
        console.error(e);
    }
}

// عملیات مدیریت بسته‌ها
async function submitAddPackage(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const res = await fetch('/api/add_package', { method: 'POST', body: formData });
    const data = await res.json();
    if(data.success) {
        alert('بسته با موفقیت اضافه شد');
        window.location.reload();
    }
}

async function deletePackage(id) {
    if(!confirm('آیا از حذف این بسته اطمینان دارید؟')) return;
    const res = await fetch('/api/delete_package/' + id, { method: 'POST' });
    const data = await res.json();
    if(data.success) {
        window.location.reload();
    }
}

async function submitAnnouncement(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const res = await fetch('/api/set_announcement', { method: 'POST', body: formData });
    const data = await res.json();
    if(data.success) {
        alert('پیام همگانی به‌روزرسانی شد');
    }
}

async function submitPrivateMsg(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const res = await fetch('/api/send_private', { method: 'POST', body: formData });
    const data = await res.json();
    if(data.success) {
        alert('پیام خصوصی ارسال شد');
        e.target.reset();
    }
}

// چرخه زمانبندی دریافت آمار اگر صفحه مدیریت باز باشد
if (window.location.pathname.includes('/admin')) {
    fetchStats();
    setInterval(fetchStats, 2000);
}
