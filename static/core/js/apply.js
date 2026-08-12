// NAVBAR CODE START
const navbar = document.getElementById("navbar");
const menuBtn = document.getElementById("menuBtn");
const mobileMenu = document.getElementById("mobileMenu");
const menuIcon = document.getElementById("menuIcon");

function getCookie(name) {
  const cookie = document.cookie.split('; ').find(row => row.startsWith(`${name}=`));
  return cookie ? decodeURIComponent(cookie.split('=').slice(1).join('=')) : null;
}

async function getCsrfToken() {
  let token = getCookie('csrftoken');
  if (token) return token;

  const response = await fetch('/api/csrf/', { credentials: 'same-origin' });
  if (!response.ok) throw new Error('Could not prepare the application form. Please refresh and try again.');

  token = getCookie('csrftoken');
  if (!token) throw new Error('Could not prepare the application form. Please refresh and try again.');
  return token;
}

// Navbar Scroll Effect
window.addEventListener("scroll", () => {

    if(window.scrollY > 8){

        navbar.classList.add("scrolled");

    }else{

        navbar.classList.remove("scrolled");

    }

});

// Mobile Menu Toggle
menuBtn.addEventListener("click", () => {

    mobileMenu.classList.toggle("show");

    if(mobileMenu.classList.contains("show")){

        menuIcon.innerHTML = "&times;";

    }else{

        menuIcon.innerHTML = "&#9776;";

    }

});

// Close mobile menu after clicking a link
document.querySelectorAll(".mobile-menu a").forEach(link=>{

    link.addEventListener("click",()=>{

        mobileMenu.classList.remove("show");

        menuIcon.innerHTML="&#9776;";

    });

});

// Active Link
const links = document.querySelectorAll(".desktop-nav a, .mobile-menu a");

links.forEach(link=>{

    if(link.href === window.location.href){

        link.classList.add("active");

    }

});
// NAVBAR CODE END


// ── Form interaction helpers ──
  function selectRadio(el, name) {
    document.querySelectorAll(`[name="${name}"]`).forEach(i => i.closest('.radio-item').classList.remove('selected'));
    el.classList.add('selected');
    el.querySelector('input').checked = true;
  }
  function toggleCheck(el) {
    el.classList.toggle('selected');
    el.querySelector('input').checked = el.classList.contains('selected');
  }
  function showReferField(show) {
    document.getElementById('referNumbers').classList.toggle('show', show);
  }

  // ── Backend submission via Fetch to Flask ──
  async function submitForm(event) {
    if (event && typeof event.preventDefault === 'function') {
      event.preventDefault();
    }

    // Validate required text fields
    const textFields = [
      { id: 'fullName', label: 'Full Name' },
      { id: 'phone', label: 'Phone Number' },
      { id: 'email', label: 'Email Address' },
      { id: 'location', label: 'City / State' },
    ];
    let valid = true;
    for (const field of textFields) {
      const el = document.getElementById(field.id);
      if (!el.value.trim()) {
        el.classList.add('error'); el.focus();
        el.addEventListener('input', () => el.classList.remove('error'), { once: true });
        alert(`Please fill in: ${field.label}`);
        return;
      }
    }
    // Validate radios
    const radioNames = ['involvement', 'attend', 'ethics', 'source', 'refer'];
    for (const name of radioNames) {
      if (!document.querySelector(`[name="${name}"]:checked`)) {
        alert('Please complete all required selections.');
        return;
      }
    }
    // Gather data
    const payload = {
      full_name: document.getElementById('fullName').value.trim(),
      phone: document.getElementById('phone').value.trim(),
      email: document.getElementById('email').value.trim(),
      location: document.getElementById('location').value.trim(),
      involvement: document.querySelector('[name="involvement"]:checked').value,
      attend_all: document.querySelector('[name="attend"]:checked').value,
      ethics_commitment: document.querySelector('[name="ethics"]:checked').value,
      heard_from: document.querySelector('[name="source"]:checked').value,
      refer_friends: document.querySelector('[name="refer"]:checked').value,
      referral_numbers: document.getElementById('referPhones')?.value?.trim() || '',
      cohort: 'Cohort 5'
    };

    // Show loading
    const btn = document.getElementById('submitBtn');
    document.getElementById('submitText').style.display = 'none';
    document.getElementById('spinner').style.display = 'block';
    btn.disabled = true;

    try {
      const csrfToken = await getCsrfToken();
      const res = await fetch('/api/applications/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'same-origin',
        body: JSON.stringify(payload)
      });
      if (!res.ok) {
        const error = await res.json().catch(() => null);
        let message = 'Submission failed. Please check your entries and try again.';
        if (error) {
          if (error.message) {
            message = error.message;
          } else if (error.non_field_errors) {
            message = Array.isArray(error.non_field_errors) ? error.non_field_errors.join(' ') : String(error.non_field_errors);
          } else {
            const allErrors = Object.values(error).flat();
            message = allErrors.length ? allErrors.join(' ') : message;
          }
        }
        throw new Error(message);
      }
      showSuccess();
      return;
    } catch (e) {
      console.error('Application submission error:', e);
      alert(e.message || 'Sorry, we could not submit your application. Please try again later.');
    } finally {
      document.getElementById('submitText').style.display = 'block';
      document.getElementById('spinner').style.display = 'none';
      document.getElementById('submitBtn').disabled = false;
    }
  }

  function showSuccess() {
    const overlay = document.getElementById('successOverlay');
    if (overlay) {
      overlay.classList.add('show');
      document.body.style.overflow = 'hidden';
    }
    // Reset button
    document.getElementById('submitText').style.display = 'block';
    document.getElementById('spinner').style.display = 'none';
    document.getElementById('submitBtn').disabled = false;
  }

  const applicationForm = document.getElementById('applicationForm');
  if (applicationForm) {
    applicationForm.addEventListener('submit', submitForm);
  }

  // Close overlay on backdrop click
  const successOverlayEl = document.getElementById('successOverlay');
  if (successOverlayEl) {
    successOverlayEl.addEventListener('click', function(e) {
      if (e.target === this) {
        this.classList.remove('show');
        document.body.style.overflow = '';
      }
    });
  }
