/**
 * Agri Gram AI - PWA Installation & Service Worker Registration Helper
 */

let deferredInstallPrompt = null;

// Register Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js', { scope: '/' })
      .then((reg) => {
        // Check for updates
        reg.addEventListener('updatefound', () => {
          const newWorker = reg.installing;
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                console.log('[PWA] New version available! Reloading...');
              }
            });
          }
        });
      })
      .catch((err) => {
        console.warn('[PWA] Service worker registration error:', err);
      });
  });
}

// Check if running as installed standalone PWA
function isRunningStandalone() {
  return window.matchMedia('(display-mode: standalone)').matches ||
         window.navigator.standalone === true ||
         document.referrer.includes('android-app://');
}

// Handle PWA Install Prompt
window.addEventListener('beforeinstallprompt', (e) => {
  // Prevent mini-infobar from appearing on mobile
  e.preventDefault();
  // Stash the event so it can be triggered later
  deferredInstallPrompt = e;
  
  // Show install UI if available
  const installBanner = document.getElementById('pwaInstallBanner');
  const installBtn = document.getElementById('pwaInstallBtn');
  if (installBanner && !isRunningStandalone()) {
    installBanner.style.display = 'flex';
  }
  if (installBtn && !isRunningStandalone()) {
    installBtn.style.display = 'inline-flex';
  }
});

// Trigger installation when user clicks Install
async function promptPWAInstall() {
  if (!deferredInstallPrompt) {
    // If browser hasn't fired beforeinstallprompt (e.g. iOS or manual)
    alert("To install Agri Gram AI on Android:\n1. Tap the three dots (⋮) in Chrome\n2. Select 'Install app' or 'Add to Home screen'");
    return;
  }
  // Show browser install dialog
  deferredInstallPrompt.prompt();
  const { outcome } = await deferredInstallPrompt.userChoice;
  console.log(`[PWA] User response to install prompt: ${outcome}`);
  deferredInstallPrompt = null;
  
  // Hide custom install banner
  const installBanner = document.getElementById('pwaInstallBanner');
  const installBtn = document.getElementById('pwaInstallBtn');
  if (installBanner) installBanner.style.display = 'none';
  if (installBtn) installBtn.style.display = 'none';
}

// App installed successfully
window.addEventListener('appinstalled', () => {
  console.log('[PWA] Agri Gram AI was installed on device!');
  deferredInstallPrompt = null;
  const installBanner = document.getElementById('pwaInstallBanner');
  const installBtn = document.getElementById('pwaInstallBtn');
  if (installBanner) installBanner.style.display = 'none';
  if (installBtn) installBtn.style.display = 'none';
});
