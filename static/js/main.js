/* ==========================================================================
   DIAGNOSTIC AI — GLOBAL JAVASCRIPT HELPERS
   ========================================================================== */

/**
 * Toggles the sidebar collapsed/expanded visual states
 * and updates local session cache.
 */
function toggleSidebar(e) {
  if (e) e.stopPropagation();
  
  var sidebar = document.getElementById('sidebar');
  var mainContent = document.getElementById('main-content');
  var toggleBtn = document.getElementById('sidebar-toggle');
  
  if (!sidebar || !mainContent || !toggleBtn) return;
  
  sidebar.classList.toggle('collapsed');
  mainContent.classList.toggle('expanded');
  
  var isCollapsed = sidebar.classList.contains('collapsed');
  
  // Set toggle button glyph or icon state
  if (toggleBtn.querySelector('[data-lucide]')) {
    // If using lucide, we let createIcons run or swap inner HTML if needed
  } else {
    toggleBtn.textContent = isCollapsed ? '›' : '‹';
  }
  
  try {
    sessionStorage.setItem('sidebarCollapsed', isCollapsed ? '1' : '0');
  } catch (err) {
    console.error('Session storage blocked:', err);
  }
}

/**
 * Toggles the mobile responsive overlay sidebar navigation.
 */
function toggleMobileSidebar(show) {
  var sidebar = document.getElementById('sidebar');
  var backdrop = document.getElementById('sidebar-backdrop');
  if (!sidebar || !backdrop) return;
  
  if (show) {
    sidebar.classList.add('mobile-open');
    backdrop.classList.add('visible');
  } else {
    sidebar.classList.remove('mobile-open');
    backdrop.classList.remove('visible');
  }
}

/**
 * Shows the custom logout confirmation modal window.
 */
function confirmLogout(e) {
  if (e) {
    e.preventDefault();
    e.stopPropagation();
  }
  var logoutModal = document.getElementById('logout-modal');
  if (logoutModal) {
    logoutModal.style.display = 'flex';
  }
}

/**
 * Closes the logout confirmation modal.
 */
function stayOnPage() {
  var logoutModal = document.getElementById('logout-modal');
  if (logoutModal) {
    logoutModal.style.display = 'none';
  }
}

/**
 * Redirects the browser to perform account logout sequence.
 */
function doLogout() {
  window.location.href = '/logout';
}

/**
 * Opens the clinical disclaimer modal.
 */
function showDisclaimerModal(e) {
  if (e) {
    e.preventDefault();
    e.stopPropagation();
  }
  var discModal = document.getElementById('disclaimer-modal');
  if (discModal) {
    discModal.style.display = 'flex';
  }
}

/**
 * Closes the clinical disclaimer modal.
 */
function closeDisclaimerModal() {
  var discModal = document.getElementById('disclaimer-modal');
  if (discModal) {
    discModal.style.display = 'none';
  }
}

// ── DOM BOOTSTRAP INITIALIZATION ──
document.addEventListener('DOMContentLoaded', function() {
  
  // 1. Restore Collapsed Sidebar State from Session Storage Cache
  try {
    if (sessionStorage.getItem('sidebarCollapsed') === '1') {
      var sidebar = document.getElementById('sidebar');
      var mainContent = document.getElementById('main-content');
      var toggleBtn = document.getElementById('sidebar-toggle');
      
      if (sidebar && mainContent && toggleBtn) {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('expanded');
        toggleBtn.textContent = '›';
      }
    }
  } catch (err) {}
  
  // 2. Collapsed Sidebar click behavior
  var sidebarEl = document.getElementById('sidebar');
  if (sidebarEl) {
    sidebarEl.addEventListener('click', function(e) {
      if (sidebarEl.classList.contains('collapsed') &&
          !e.target.closest('#sidebar-toggle') &&
          !e.target.closest('a')) {
        toggleSidebar();
      }
    });
  }
  
  // 3. Close Logout Modal on backdrop click
  var logoutModalEl = document.getElementById('logout-modal');
  if (logoutModalEl) {
    logoutModalEl.addEventListener('click', function(e) {
      if (e.target === this) {
        stayOnPage();
      }
    });
  }

  // 4. Close Disclaimer Modal on backdrop click
  var discModalEl = document.getElementById('disclaimer-modal');
  if (discModalEl) {
    discModalEl.addEventListener('click', function(e) {
      if (e.target === this) {
        closeDisclaimerModal();
      }
    });
  }
  
  // 5. Instantiates Lucide vector icons
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
});
