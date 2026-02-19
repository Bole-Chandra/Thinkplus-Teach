const API_URL = 'http://127.0.0.1:8000/api';

// Simple state management
let currentRole = 'student';

// Auth Form Toggling
if (document.getElementById('showRegister')) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const showRegister = document.getElementById('showRegister');
    const showLogin = document.getElementById('showLogin');
    const authMessage = document.getElementById('authMessage');

    showRegister.onclick = (e) => {
        e.preventDefault();
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        authMessage.innerText = '';
    };

    showLogin.onclick = (e) => {
        e.preventDefault();
        registerForm.style.display = 'none';
        loginForm.style.display = 'block';
        authMessage.innerText = '';
    };

    // Role Selection
    const studentBtn = document.getElementById('studentBtn');
    const instructorBtn = document.getElementById('instructorBtn');

    studentBtn.onclick = () => {
        currentRole = 'student';
        studentBtn.classList.add('active');
        instructorBtn.classList.remove('active');
    };

    instructorBtn.onclick = () => {
        currentRole = 'instructor';
        instructorBtn.classList.add('active');
        studentBtn.classList.remove('active');
    };

    // Login Submission
    loginForm.onsubmit = async (e) => {
        e.preventDefault();
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const res = await fetch(`${API_URL}/users/login/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await res.json();

            if (res.ok) {
                localStorage.setItem('user', JSON.stringify(data));
                localStorage.setItem('role', data.role);
                window.location.href = data.role === 'instructor' ? 'dashboard_instructor.html' : 'dashboard_student.html';
            } else {
                authMessage.innerText = data.error || 'Login Failed';
            }
        } catch (e) {
            authMessage.innerText = 'Connection Error';
        }
    };

    // Register Submission
    registerForm.onsubmit = async (e) => {
        e.preventDefault();
        const username = document.getElementById('regUsername').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;

        try {
            const res = await fetch(`${API_URL}/users/register/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password, role: currentRole })
            });
            const data = await res.json();

            if (res.ok) {
                authMessage.style.color = '#86efac';
                authMessage.innerText = 'Registration Successful! Please Sign In.';
                setTimeout(() => showLogin.click(), 2000);
            } else {
                authMessage.style.color = '#ff8080';
                authMessage.innerText = Object.values(data).join(', ');
            }
        } catch (e) {
            authMessage.innerText = 'Connection Error';
        }
    };
}

// Student Dashboard Logic
async function loadStudentDashboard() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) return window.location.href = 'index.html';
    document.getElementById('userName').innerText = user.username;

    // Load Assignments
    try {
        const res = await fetch(`${API_URL}/assignments/`);
        const assignments = await res.json();
        const list = document.getElementById('assignmentList');
        list.innerHTML = assignments.map(a => `
            <div class="card">
                <h3>${a.title}</h3>
                <p>${a.description}</p>
                <button onclick="showSubmitModal(${a.id})" class="primary-btn" style="width: auto; padding: 8px 16px;">Submit Work</button>
            </div>
        `).join('');
    } catch (e) { console.error(e); }

    // Load Student's Submissions (History)
    try {
        const res = await fetch(`${API_URL}/submissions/`);
        const submissions = await res.json();
        const myList = submissions.filter(s => s.student == user.id);
        const container = document.getElementById('studentSubmissions');

        if (myList.length === 0) {
            container.innerHTML = '<p class="footer-text">No submissions yet.</p>';
        } else {
            container.innerHTML = myList.map(s => `
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4>Assignment ID: ${s.assignment}</h4>
                        <span class="badge ${s.plagiarism_score > 30 ? 'badge-risk' : 'badge-good'}">
                            Risk: ${s.plagiarism_score.toFixed(1)}%
                        </span>
                    </div>
                    <p style="margin: 10px 0; font-size: 0.9rem; color: var(--text-muted);">
                        <strong>AI Review:</strong> ${s.feedback || '⏳ Evaluation in progress...'}
                    </p>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 600;">
                        <span>Grade: ${s.grade}/100 | Status: ${s.is_evaluated ? '✅ Evaluated' : '⏳ Pending'}</span>
                        <span style="color: var(--primary)">${new Date(s.submitted_at).toLocaleDateString()}</span>
                    </div>
                </div>
            `).join('');
        }
    } catch (e) { console.error(e); }
}

// Instructor Dashboard Logic
async function loadInstructorDashboard() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) return window.location.href = 'index.html';
    document.getElementById('userName').innerText = user.username;

    loadSubmissions();
}

async function loadSubmissions() {
    try {
        const res = await fetch(`${API_URL}/submissions/`);
        const submissions = await res.json();
        const list = document.getElementById('submissionList');
        list.innerHTML = submissions.map(s => `
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4>${s.student_name} (ID: ${s.student})</h4>
                    <span class="badge ${s.plagiarism_score > 30 ? 'badge-risk' : 'badge-good'}">
                        Plagiarism: ${s.plagiarism_score.toFixed(1)}%
                    </span>
                </div>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Assignment ID: ${s.assignment}</p>
                <p style="margin: 12px 0;"><strong>AI Feedback:</strong> ${s.feedback || 'Evaluating...'}</p>
                <div style="display: flex; gap: 10px; font-size: 0.9rem; color: var(--text-muted);">
                    <span>Score: ${s.grade}/100</span>
                    <span>Status: ${s.is_evaluated ? '✅ Completed' : '⏳ Pending'}</span>
                </div>
            </div>
        `).join('');
    } catch (e) {
        console.error("Error loading submissions", e);
    }
}

async function createAssignment(e) {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const user = JSON.parse(localStorage.getItem('user'));

    const data = {
        title,
        description,
        created_by: user.id
    };

    await fetch(`${API_URL}/assignments//`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    alert('Assignment Created!');
    location.reload();
}

async function submitAssignment(e) {
    e.preventDefault();
    const textContent = document.getElementById('textContent').value;
    const assignmentId = document.getElementById('assignmentId').value;
    const user = JSON.parse(localStorage.getItem('user'));

    const data = {
        student: user.id,
        assignment: assignmentId,
        text_content: textContent
    };

    await fetch(`${API_URL}/submissions//`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    alert('Assignment Submitted! AI is evaluating...');
    location.reload();
}

function logout() {
    localStorage.clear();
    window.location.href = 'index.html';
}
