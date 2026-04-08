/* ═══════════════════════════════════════════════════════════
   FOODIE — Main JavaScript
   Features: Page loader, Navbar scroll, AJAX cart,
             Toast messages, Animations, Scroll reveal
═══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

  // ─── 1. PAGE LOADER ─────────────────────────────────────
  const loader = document.getElementById('page-loader');
  if (loader) {
    window.addEventListener('load', () => {
      setTimeout(() => loader.classList.add('hidden'), 300);
    });
    // Fallback: hide after 2.5s even if load doesn't fire
    setTimeout(() => loader.classList.add('hidden'), 2500);
  }


  // ─── 2. NAVBAR SCROLL EFFECT ────────────────────────────
  const navbar = document.getElementById('mainNavbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.3)';
        navbar.style.padding = '6px 0';
      } else {
        navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,0.2)';
        navbar.style.padding = '10px 0';
      }
    });
  }


  // ─── 3. AJAX ADD TO CART ────────────────────────────────
  const csrfToken = getCsrfToken();

  document.querySelectorAll('.add-to-cart-form').forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const btn = this.querySelector('.btn-add-cart');
      const foodId = btn.dataset.foodId;
      const foodName = btn.dataset.foodName;

      // Loading state
      btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
      btn.disabled = true;

      fetch(this.action, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest',
        },
      })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          // Success state
          btn.innerHTML = '<i class="bi bi-check-lg"></i><span>Added!</span>';
          btn.classList.add('added');

          // Update cart badge
          updateCartBadge(data.cart_total);

          // Show toast
          showToast(`✅ ${foodName} added to cart!`, 'success');

          // Reset button after delay
          setTimeout(() => {
            btn.innerHTML = '<i class="bi bi-plus-lg"></i><span>Add</span>';
            btn.classList.remove('added');
            btn.disabled = false;
          }, 1500);
        }
      })
      .catch(() => {
        btn.innerHTML = '<i class="bi bi-plus-lg"></i><span>Add</span>';
        btn.disabled = false;
        showToast('❌ Error adding to cart', 'danger');
      });
    });
  });


  // ─── 4. SCROLL REVEAL ANIMATION ─────────────────────────
  const revealElements = document.querySelectorAll(
    '.food-card, .category-card, .how-card, .order-history-card'
  );

  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry, i) => {
          if (entry.isIntersecting) {
            setTimeout(() => {
              entry.target.classList.add('fade-in-up');
            }, i * 80);
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    revealElements.forEach(el => revealObserver.observe(el));
  }


  // ─── 5. AUTO-DISMISS ALERTS ─────────────────────────────
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      if (alert && alert.parentNode) {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 300);
      }
    }, 4000);
  });


  // ─── 6. SMOOTH SCROLL FOR ANCHOR LINKS ──────────────────
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });


  // ─── 7. FORM VALIDATION FEEDBACK ────────────────────────
  document.querySelectorAll('form[novalidate]').forEach(form => {
    form.addEventListener('submit', function (e) {
      if (!this.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();
        // Highlight invalid fields
        this.querySelectorAll(':invalid').forEach(field => {
          field.classList.add('is-invalid');
        });
      }
      this.classList.add('was-validated');
    });
    // Remove invalid class on input
    form.querySelectorAll('input, textarea, select').forEach(field => {
      field.addEventListener('input', function () {
        this.classList.remove('is-invalid');
      });
    });
  });


  // ─── 8. ACTIVE NAV LINK INDICATOR ───────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });


  // ─── 9. IMAGE LAZY LOADING FALLBACK ─────────────────────
  document.querySelectorAll('img[loading="lazy"]').forEach(img => {
    img.addEventListener('error', function () {
      this.src = 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&q=80';
    });
  });

});


// ═══════════════════════════════════════════════════════════
// HELPER FUNCTIONS
// ═══════════════════════════════════════════════════════════

/** Get CSRF token from cookie */
function getCsrfToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : '';
}

/** Update cart badge count in navbar */
function updateCartBadge(count) {
  let badge = document.querySelector('.cart-badge');
  const cartLink = document.querySelector('.cart-link');
  if (!cartLink) return;

  if (count > 0) {
    if (!badge) {
      badge = document.createElement('span');
      badge.className = 'cart-badge';
      cartLink.appendChild(badge);
    }
    badge.textContent = count;
    // Bounce animation
    badge.style.animation = 'none';
    badge.offsetHeight; // Force reflow
    badge.style.animation = 'cartBounce 0.4s ease';
  } else if (badge) {
    badge.remove();
  }
}

/** Show toast notification */
function showToast(message, type = 'success') {
  // Create toast container if missing
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.style.cssText = `
      position:fixed; top:80px; right:20px;
      z-index:9999; display:flex; flex-direction:column; gap:10px;
    `;
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `alert alert-${type} shadow-lg border-0 mb-0 rounded-3 d-flex align-items-center`;
  toast.style.cssText = 'animation: slideInRight .3s ease; min-width:250px; max-width:350px;';
  toast.innerHTML = `
    ${message}
    <button type="button" class="btn-close ms-auto" onclick="this.parentElement.remove()"></button>
  `;

  container.appendChild(toast);

  // Auto remove after 3s
  setTimeout(() => {
    toast.style.animation = 'fadeOut .3s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Additional CSS injected for toast animation
const style = document.createElement('style');
style.textContent = `
  @keyframes slideInRight {
    from { opacity:0; transform:translateX(100%); }
    to   { opacity:1; transform:translateX(0); }
  }
  @keyframes fadeOut {
    from { opacity:1; }
    to   { opacity:0; transform:translateX(20px); }
  }
`;
document.head.appendChild(style);
