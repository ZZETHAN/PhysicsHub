/**
 * PhysicsHub 认证系统 - 前端模块
 * 功能：登录、注册、Token管理、访问控制
 */

const API_BASE_URL = 'http://123.207.75.145:3001/api';

// ========== Token 管理 ==========
const Auth = {
    // 获取 Token
    getToken() {
        return localStorage.getItem('physicshub_token');
    },

    // 设置 Token
    setToken(token) {
        localStorage.setItem('physicshub_token', token);
    },

    // 清除 Token
    clearToken() {
        localStorage.removeItem('physicshub_token');
        localStorage.removeItem('physicshub_user');
    },

    // 获取当前用户
    getUser() {
        const user = localStorage.getItem('physicshub_user');
        return user ? JSON.parse(user) : null;
    },

    // 设置当前用户
    setUser(user) {
        localStorage.setItem('physicshub_user', JSON.stringify(user));
    },

    // 检查是否登录
    isLoggedIn() {
        return !!this.getToken();
    },

    // 检查是否是管理员
    isAdmin() {
        const user = this.getUser();
        return user && user.role === 'admin';
    },

    // 退出登录
    logout() {
        console.log('Logging out...');
        // 清除所有存储的数据
        localStorage.removeItem('physicshub_token');
        localStorage.removeItem('physicshub_user');
        console.log('Token cleared:', !localStorage.getItem('physicshub_token'));
        // 立即刷新页面
        window.location.href = window.location.href;
    }
};

// ========== API 请求 ==========
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const token = Auth.getToken();
    
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        },
        ...options
    };

    if (config.body && typeof config.body === 'object') {
        config.body = JSON.stringify(config.body);
    }

    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ========== 登录/注册 ==========
const AuthAPI = {
    // 登录
    async login(username, password) {
        const data = await apiRequest('/auth/login', {
            method: 'POST',
            body: { username, password }
        });
        
        if (data.success) {
            Auth.setToken(data.token);
            Auth.setUser(data.user);
        }
        
        return data;
    },

    // 注册
    async register(username, email, password) {
        return await apiRequest('/auth/register', {
            method: 'POST',
            body: { username, email, password }
        });
    },

    // 获取当前用户信息
    async getCurrentUser() {
        return await apiRequest('/auth/me');
    },

    // 退出登录 (调用 Auth.logout)
    logout() {
        Auth.logout();
    }
};

// ========== UI 更新 ==========
function updateAuthUI() {
    const authBtn = document.getElementById('authBtn');
    const userInfo = document.getElementById('userInfo');
    
    if (!authBtn) return;

    if (Auth.isLoggedIn()) {
        const user = Auth.getUser();
        const isAdmin = Auth.isAdmin();
        
        const avatarIcon = user.avatar_icon || user.username.charAt(0).toUpperCase();
        const avatarBg = user.avatar_color || '#0891b2';
        
        // 简洁设计：点击头像/名字进入个人中心
        const basePath = window.location.pathname.includes('/units/') ? '../../' : './';
        authBtn.innerHTML = `
            <a href="${basePath}profile.html" class="user-profile-link">
                <span class="user-avatar" style="background: linear-gradient(135deg, ${avatarBg}, ${avatarBg}dd);">${avatarIcon}</span>
                <span class="user-name">${user.username}</span>
            </a>
        `;
        
        if (userInfo) userInfo.innerHTML = '';
    } else {
        authBtn.innerHTML = `
            <a href="#" class="login-link" onclick="AuthModal.open(); return false;">
                <span class="login-text">Login</span>
            </a>
        `;
        if (userInfo) userInfo.innerHTML = '';
    }
}

// ========== 访问控制 ==========
function checkAuth() {
    if (!Auth.isLoggedIn()) {
        AuthModal.open();
        return false;
    }
    return true;
}

// 保护页面 - 需要登录才能访问
function protectPage() {
    if (Auth.isLoggedIn()) {
        // 已登录，显示内容
        document.body.classList.add('auth-verified');
        return true;
    }
    
    // 未登录，模糊/隐藏内容，显示登录提示
    document.body.classList.add('auth-required');
    
    // 创建强制登录遮罩（不能通过关闭弹窗绕过）
    const overlay = document.createElement('div');
    overlay.id = 'authOverlay';
    overlay.innerHTML = `
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(248, 250, 252, 0.98);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            flex-direction: column;
            padding: 16px;
            overflow-y: auto;
        ">
            <div id="authOverlayContent" style="
                background: white;
                padding: 32px 24px;
                border-radius: 16px;
                text-align: center;
                max-width: 360px;
                width: 100%;
                box-shadow: 0 20px 40px -12px rgba(0,0,0,0.15);
            ">
                <div style="font-size: 44px; margin-bottom: 12px;">🔒</div>
<h2 style="margin: 0 0 10px 0; color: #1e293b; font-size: 20px;">Login Required</h2>
                    <p style="color: #475569; font-size: 14px; margin: 0 0 20px 0;">
                        Please login to access the content.<br>
                    No account yet? Registration requires admin approval.
                </p>
                <button onclick="AuthModal.open()" style="
                    background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 10px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: 600;
                    margin-bottom: 10px;
                    width: 100%;
                ">Login / Register</button>
                <a href="../../index.html" style="
                    color: #64748b;
                    text-decoration: none;
                    font-size: 13px;
                    display: inline-block;
                    margin-top: 6px;
                ">← Back to Home</a>
            </div>
        </div>
    `;
    document.body.appendChild(overlay);
    
    // 模糊页面内容
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.style.filter = 'blur(8px)';
        mainContent.style.pointerEvents = 'none';
        mainContent.style.userSelect = 'none';
    }
    
    return false;
}

// ========== 登录/注册弹窗 ==========
const AuthModal = {
    modal: null,

    create() {
        if (this.modal) return this.modal;

        const modal = document.createElement('div');
        modal.id = 'authModal';
        modal.innerHTML = `
            <div class="auth-modal-overlay">
                <div class="auth-modal-container">
                    <!-- 强制登录模式下隐藏关闭按钮 -->
                    
                    <div class="auth-tabs">
                        <button class="auth-tab active" data-tab="login">Login</button>
                        <button class="auth-tab" data-tab="register">Register</button>
                    </div>
                    
                    <!-- 登录表单 -->
                    <form id="loginForm" class="auth-form active">
                        <div class="auth-input-group">
                            <label>Username or Email</label>
                            <input type="text" name="username" placeholder="Enter username or email" required>
                        </div>
                        <div class="auth-input-group">
                            <label>Password</label>
                            <div class="auth-password-wrapper">
                                <input type="password" name="password" id="loginPassword" placeholder="Enter password" required>
                                <button type="button" class="auth-password-toggle" onclick="AuthModal.togglePassword('loginPassword')" title="Show/Hide Password">
                                    👁️
                                </button>
                            </div>
                        </div>
                        <button type="submit" class="auth-submit-btn">Login</button>
                        <div class="auth-message" id="loginMessage"></div>
                    </form>
                    
                    <!-- 注册表单 -->
                    <form id="registerForm" class="auth-form">
                        <div class="auth-input-group">
                            <label>Username</label>
                            <input type="text" name="username" placeholder="3-20 characters" required minlength="3" maxlength="20">
                        </div>
                        <div class="auth-input-group">
                            <label>Email</label>
                            <input type="email" name="email" placeholder="your@email.com" required>
                        </div>
                        <div class="auth-input-group">
                            <label>Password</label>
                            <div class="auth-password-wrapper">
                                <input type="password" name="password" id="registerPassword" placeholder="At least 6 characters" required minlength="6">
                                <button type="button" class="auth-password-toggle" onclick="AuthModal.togglePassword('registerPassword')" title="Show/Hide Password">
                                    👁️
                                </button>
                            </div>
                        </div>
                        <div class="auth-notice">
                            💡 Registration requires admin approval before you can login
                        </div>
                        <button type="submit" class="auth-submit-btn">Register</button>
                        <div class="auth-message" id="registerMessage"></div>
                    </form>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        this.modal = modal;
        this.bindEvents();
        return modal;
    },

    bindEvents() {
        // Tab 切换
        const tabs = this.modal.querySelectorAll('.auth-tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                const forms = this.modal.querySelectorAll('.auth-form');
                forms.forEach(f => f.classList.remove('active'));
                this.modal.querySelector(`#${tab.dataset.tab}Form`).classList.add('active');
            });
        });

        // 登录表单提交
        const loginForm = this.modal.querySelector('#loginForm');
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);
            const messageEl = document.getElementById('loginMessage');
            
            try {
                const data = await AuthAPI.login(
                    formData.get('username'),
                    formData.get('password')
                );
                
                messageEl.textContent = 'Login successful!';
                messageEl.className = 'auth-message success';
                
                setTimeout(() => {
                    this.close();
                    updateAuthUI();
                    // 刷新页面以显示内容
                    location.reload();
                }, 500);
            } catch (error) {
                messageEl.textContent = error.message || 'Login failed';
                messageEl.className = 'auth-message error';
            }
        });

        // 注册表单提交
        const registerForm = this.modal.querySelector('#registerForm');
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(registerForm);
            const messageEl = document.getElementById('registerMessage');
            
            try {
                const data = await AuthAPI.register(
                    formData.get('username'),
                    formData.get('email'),
                    formData.get('password')
                );
                
                messageEl.textContent = data.message;
                messageEl.className = 'auth-message success';
                
                // 切换到登录Tab
                setTimeout(() => {
                    this.modal.querySelector('[data-tab="login"]').click();
                }, 2000);
            } catch (error) {
                messageEl.textContent = error.message || 'Registration failed';
                messageEl.className = 'auth-message error';
            }
        });
    },

    open() {
        const modal = this.create();
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    },

    close() {
        if (this.modal) {
            this.modal.style.display = 'none';
            document.body.style.overflow = '';
        }
        
        // 如果未登录，保持遮罩显示（不允许关闭弹窗绕过登录）
        if (!Auth.isLoggedIn()) {
            // 保持遮罩层显示
            const overlay = document.getElementById('authOverlay');
            if (overlay) {
                overlay.style.display = 'flex';
            }
        }
    },

    // 切换密码显示/隐藏
    togglePassword(inputId) {
        const input = document.getElementById(inputId);
        const button = input.nextElementSibling;
        
        if (input.type === 'password') {
            input.type = 'text';
            button.textContent = '🙈';
button.title = 'Hide Password';
            } else {
                button.title = 'Show Password';
        }
    }
};

// ========== 页面加载时初始化 ==========
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    
    // 如果是教学页面，检查登录状态
    const isUnitPage = window.location.pathname.includes('/units/ch');
    if (isUnitPage) {
        protectPage();
    }
});

// ========== 跨Tab同步头像等用户数据 ==========
window.addEventListener('storage', (e) => {
    // 只监听 physicshub_user 的变化（头像、用户名等）
    if (e.key === 'physicshub_user' && e.newValue) {
        try {
            const newUser = JSON.parse(e.newValue);
            // 更新 Auth 模块的缓存
            Auth.setUser(newUser);
            // 刷新UI
            if (typeof updateAuthUI === 'function') {
                updateAuthUI();
            }
        } catch (err) {
            console.error('Failed to parse user data from storage event:', err);
        }
    }
    // Token 变化时（登录/登出）
    if (e.key === 'physicshub_token') {
        if (typeof updateAuthUI === 'function') {
            updateAuthUI();
        }
    }
});

// 导出供全局使用
window.Auth = Auth;
window.AuthAPI = AuthAPI;
window.AuthModal = AuthModal;
window.updateAuthUI = updateAuthUI;
window.checkAuth = checkAuth;
window.protectPage = protectPage;
