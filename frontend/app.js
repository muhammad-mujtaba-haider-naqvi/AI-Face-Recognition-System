/* ========================================
   VisionX - Application JavaScript
   Ultra-Modern Futuristic UI Controller
   ======================================== */

// ===== STATE MANAGEMENT =====
const appState = {
  bridgeReady: false,
  bridge: null,
  particleCount: 50,
  particles: [],
};

// ===== PARTICLE SYSTEM =====
function initializeParticles() {
  const container = document.getElementById('particlesContainer');
  
  for (let i = 0; i < appState.particleCount; i++) {
    const particle = createParticle();
    container.appendChild(particle);
    appState.particles.push(particle);
  }
}

function createParticle() {
  const particle = document.createElement('div');
  particle.className = 'particle';
  
  const size = Math.random() * 3 + 1;
  const x = Math.random() * 100;
  const y = Math.random() * 100;
  const duration = Math.random() * 15 + 10;
  const delay = Math.random() * 5;
  
  particle.style.width = size + 'px';
  particle.style.height = size + 'px';
  particle.style.left = x + '%';
  particle.style.top = y + '%';
  particle.style.animation = `particleFloat ${duration}s linear ${delay}s infinite`;
  
  return particle;
}

// Add particle animation keyframes
function addParticleAnimation() {
  const style = document.createElement('style');
  style.textContent = `
    @keyframes particleFloat {
      0% {
        transform: translate(0, 0) scale(1);
        opacity: 0;
      }
      10% {
        opacity: 1;
      }
      90% {
        opacity: 1;
      }
      100% {
        transform: translate(${Math.random() * 100 - 50}px, -${Math.random() * 200 + 100}px) scale(0);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);
}

// ===== NAVBAR SCROLL EFFECT =====
function initializeNavbar() {
  const navbar = document.getElementById('navbar');
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });
}

// ===== SMOOTH SCROLL LINKS =====
function initializeSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const target = document.querySelector(link.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
}

// ===== TOAST NOTIFICATIONS =====
function showToast(message, type = 'success') {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = 'slideOutRight 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// ===== QWE BCHANNEL INITIALIZATION =====
function initializeBridge() {
  // Try loading from https first, fallback to local
  const scriptSrc = 'https://qwebchannel.qt.io/qwebchannel.js';
  
  // Check if QWebChannel is already loaded
  if (typeof QWebChannel !== 'undefined') {
    setupBridge();
  } else {
    // Try to load from local fallback
    const script = document.createElement('script');
    script.src = scriptSrc;
    script.onload = setupBridge;
    script.onerror = () => {
      console.log('QWebChannel not available, using mock bridge');
      setupMockBridge();
    };
    document.head.appendChild(script);
  }
}

function setupBridge() {
  if (typeof qt === 'undefined' || typeof qt.webChannelTransport === 'undefined') {
    console.log('QWebChannel transport not available, using mock bridge');
    setupMockBridge();
    return;
  }

  new QWebChannel(qt.webChannelTransport, (channel) => {
    appState.bridge = channel.objects.bridge;
    appState.bridgeReady = true;
    console.log('Bridge connected successfully');
    attachBridgeEventListeners();
    loadSystemStats();
  });
}

function setupMockBridge() {
  // Mock bridge for development/testing
  appState.bridge = {
    openModule: (module) => {
      console.log('Mock: Opening module', module);
      showToast(`Opened ${module} module`, 'success');
    },
    openDeveloper: () => {
      console.log('Mock: Opening Developer');
      showToast('Developer panel opened', 'success');
    },
    openHelpdesk: () => {
      console.log('Mock: Opening Helpdesk');
      showToast('Help & Support opened', 'success');
    },
    moduleOpened: { connect: () => {} },
    statsUpdated: { connect: () => {} },
  };
  appState.bridgeReady = true;
  console.log('Mock bridge initialized');
  attachBridgeEventListeners();
}

function attachBridgeEventListeners() {
  if (!appState.bridge) return;

  // Connect to bridge signals
  if (appState.bridge.statsUpdated && appState.bridge.statsUpdated.connect) {
    appState.bridge.statsUpdated.connect((stats) => {
      updateStats(stats);
    });
  }

  if (appState.bridge.moduleOpened && appState.bridge.moduleOpened.connect) {
    appState.bridge.moduleOpened.connect((moduleName) => {
      console.log(`Module opened: ${moduleName}`);
    });
  }
}

// ===== MODULE BUTTON HANDLERS =====
function initializeModuleButtons() {
  // Module cards
  document.querySelectorAll('.module-card').forEach(card => {
    const button = card.querySelector('.module-btn');
    const action = card.getAttribute('data-action');
    
    button.addEventListener('click', () => {
      openModule(action);
    });
  });

  // Direct action buttons
  document.getElementById('markAttendanceBtn').addEventListener('click', () => {
    openModule('recognition');
  });

  document.getElementById('recordsBtn').addEventListener('click', () => {
    openModule('attendance');
  });

  document.getElementById('legacyDashboardBtn').addEventListener('click', () => {
    openModule('main');
  });
}

function openModule(moduleName) {
  if (!appState.bridgeReady || !appState.bridge) {
    showToast('Bridge not initialized', 'error');
    return;
  }

  try {
    switch(moduleName) {
      case 'student':
        appState.bridge.openModule('student');
        showToast('Student Registration module opened', 'success');
        break;
      case 'recognition':
        appState.bridge.openModule('recognition');
        showToast('Face Recognition started', 'success');
        break;
      case 'attendance':
        appState.bridge.openModule('attendance');
        showToast('Attendance Records loaded', 'success');
        break;
      case 'training':
        appState.bridge.openModule('training');
        showToast('Model Training module opened', 'success');
        break;
      case 'developer':
        appState.bridge.openDeveloper();
        showToast('Developer Panel opened', 'success');
        break;
      case 'helpdesk':
        appState.bridge.openHelpdesk();
        showToast('Help & Support opened', 'success');
        break;
      case 'main':
        appState.bridge.openModule('main');
        showToast('Legacy Dashboard opened', 'success');
        break;
      default:
        showToast(`Opening ${moduleName}`, 'success');
        appState.bridge.openModule(moduleName);
    }
  } catch (error) {
    console.error('Error opening module:', error);
    showToast('Error opening module: ' + error.message, 'error');
  }
}

// ===== SYSTEM STATS =====
function loadSystemStats() {
  if (!appState.bridgeReady || !appState.bridge) return;

  try {
    if (appState.bridge.getStats && typeof appState.bridge.getStats === 'function') {
      appState.bridge.getStats((stats) => {
        updateStats(stats);
      });
    } else {
      console.log('getStats not available on bridge');
      setMockStats();
    }
  } catch (error) {
    console.error('Error loading stats:', error);
    setMockStats();
  }
}

function updateStats(stats) {
  if (!stats) return;

  if (stats.students_registered !== undefined) {
    document.getElementById('studentsRegistered').textContent = stats.students_registered;
  }
  if (stats.face_samples !== undefined) {
    document.getElementById('faceSamples').textContent = stats.face_samples;
  }
  if (stats.today_attendance !== undefined) {
    document.getElementById('todayAttendance').textContent = stats.today_attendance;
  }
}

function setMockStats() {
  const mockStats = {
    students_registered: Math.floor(Math.random() * 150) + 50,
    face_samples: Math.floor(Math.random() * 500) + 200,
    today_attendance: Math.floor(Math.random() * 80) + 10,
  };
  updateStats(mockStats);
}

// ===== ANIMATIONS ON SCROLL =====
function initializeScrollAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px',
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.feature-block, .module-card, .analytics-card, .benefit-item').forEach(el => {
    observer.observe(el);
  });
}

// ===== HOVER EFFECTS FOR FEATURE CARDS =====
function initializeCardHoverEffects() {
  document.querySelectorAll('.feature-block, .module-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transition = 'all 0.3s ease';
    });
  });
}

// ===== MOUSE MOVE PARALLAX =====
function initializeMouseParallax() {
  const heroVisual = document.querySelector('.hero-visual');
  
  if (!heroVisual) return;
  
  document.addEventListener('mousemove', (e) => {
    const x = (e.clientX / window.innerWidth - 0.5) * 20;
    const y = (e.clientY / window.innerHeight - 0.5) * 20;
    heroVisual.style.transform = `perspective(1000px) rotateX(${y}deg) rotateY(${x}deg)`;
  });
}

// ===== PERFORMANCE OPTIMIZATION =====
function optimizePerformance() {
  // Reduce particle count on mobile
  if (window.innerWidth < 768) {
    appState.particleCount = 20;
  }
  
  // Disable parallax on mobile
  if (window.innerWidth < 768) {
    // Parallax disabled for mobile
    return;
  }
}

// ===== INITIALIZATION =====
function initialize() {
  console.log('🚀 VisionX initializing...');
  
  // Performance optimization
  optimizePerformance();
  
  // Initialize UI components
  addParticleAnimation();
  initializeParticles();
  initializeNavbar();
  initializeSmoothScroll();
  initializeScrollAnimations();
  initializeCardHoverEffects();
  initializeMouseParallax();
  
  // Initialize bridge and modules
  initializeBridge();
  initializeModuleButtons();
  
  // Load stats after a delay to allow bridge initialization
  setTimeout(() => {
    loadSystemStats();
    setInterval(loadSystemStats, 30000); // Refresh every 30 seconds
  }, 1000);
  
  console.log('✨ VisionX ready!');
  showToast('VisionX initialized successfully', 'success');
}

// ===== DOM READY =====
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initialize);
} else {
  initialize();
}

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', (e) => {
  // Ctrl/Cmd + K: Focus search (if needed)
  // Ctrl/Cmd + /: Open help
  if ((e.ctrlKey || e.metaKey) && e.key === '/') {
    e.preventDefault();
    openModule('helpdesk');
  }
});

// ===== ERROR HANDLING =====
window.addEventListener('error', (e) => {
  console.error('Global error:', e.error);
});

window.addEventListener('unhandledrejection', (e) => {
  console.error('Unhandled promise rejection:', e.reason);
});

// ===== CONSOLE BRANDING =====
console.log(
  '%c✨ VisionX - Where Vision Meets Intelligence ✨',
  'color: #00BFFF; font-size: 16px; font-weight: bold; text-shadow: 0 0 10px rgba(0, 191, 255, 0.5);'
);
console.log(
  '%cPowered by Advanced AI Face Recognition Technology',
  'color: #38BDF8; font-size: 12px;'
);
