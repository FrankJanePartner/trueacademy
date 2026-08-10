// NAVBAR CODE START
const navbar = document.getElementById("navbar");
const menuBtn = document.getElementById("menuBtn");
const mobileMenu = document.getElementById("mobileMenu");
const menuIcon = document.getElementById("menuIcon");

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

  async function submitContactForm(event) {
    event.preventDefault();
    const textFields = [
      { id: 'fullName', label: 'Full Name' },
      { id: 'email', label: 'Email Address' },
      { id: 'phone', label: 'Phone Number' },
      { id: 'message', label: 'Message' },
    ];
    for (const field of textFields) {
      const el = document.getElementById(field.id);
      if (!el || !el.value.trim()) {
        alert(`Please fill in: ${field.label}`);
        if (el) {
          el.classList.add('error');
          el.focus();
          el.addEventListener('input', () => el.classList.remove('error'), { once: true });
        }
        return;
      }
    }

    const payload = {
      full_name: document.getElementById('fullName').value.trim(),
      email: document.getElementById('email').value.trim(),
      phone: document.getElementById('phone').value.trim(),
      subject: document.getElementById('subject').value.trim(),
      message: document.getElementById('message').value.trim(),
    };

    const form = event.currentTarget;
    const btn = form.querySelector('button[type="submit"]');
    if (btn) btn.disabled = true;

    try {
      const res = await fetch('/api/contact/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const error = await res.json().catch(() => null);
        throw new Error(error?.detail || 'Submission failed');
      }
      alert('Your message has been sent successfully.');
      form.reset();
    } catch (error) {
      console.error('Contact submission error:', error);
      alert('Sorry, there was a problem sending your message. Please try again later.');
    } finally {
      if (btn) btn.disabled = false;
    }
  }

  async function submitForm() {
    const textFields = [
      { id: 'fullName', label: 'Full Name' },
      { id: 'phone', label: 'Phone Number' },
      { id: 'email', label: 'Email Address' },
      { id: 'location', label: 'City / State' },
      { id: 'challenge', label: 'Biggest Challenge' },
    ];
    for (const field of textFields) {
      const el = document.getElementById(field.id);
      if (!el.value.trim()) {
        el.classList.add('error'); el.focus();
        el.addEventListener('input', () => el.classList.remove('error'), { once: true });
        alert(`Please fill in: ${field.label}`);
        return;
      }
    }

    const radioNames = ['involvement', 'experience', 'attend', 'ethics', 'source', 'refer', 'interest'];
    for (const name of radioNames) {
      if (!document.querySelector(`[name="${name}"]:checked`)) {
        alert('Please complete all required selections.');
        return;
      }
    }

    const interests = [...document.querySelectorAll('[name="interest"]:checked')].map(i => i.value);
    if (interests.length === 0) {
      alert('Please select at least one area of real estate interest.');
      return;
    }

    const payload = {
      full_name: document.getElementById('fullName').value.trim(),
      phone: document.getElementById('phone').value.trim(),
      email: document.getElementById('email').value.trim(),
      location: document.getElementById('location').value.trim(),
      involvement: document.querySelector('[name="involvement"]:checked').value,
      experience: document.querySelector('[name="experience"]:checked').value,
      interests,
      challenge: document.getElementById('challenge').value.trim(),
      attend_all: document.querySelector('[name="attend"]:checked').value,
      ethics_commitment: document.querySelector('[name="ethics"]:checked').value,
      heard_from: document.querySelector('[name="source"]:checked').value,
      refer_friends: document.querySelector('[name="refer"]:checked').value,
      referral_numbers: document.getElementById('referPhones')?.value?.trim() || '',
      cohort: 'Cohort 4'
    };

    const btn = document.getElementById('submitBtn');
    document.getElementById('submitText').style.display = 'none';
    document.getElementById('spinner').style.display = 'block';
    btn.disabled = true;

    try {
      const res = await fetch('/api/applications/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) {
        const error = await res.json().catch(() => null);
        throw new Error(error?.detail || 'Submission failed');
      }
      showSuccess();
      return;
    } catch (err) {
      console.error('Application submission error:', err);
      alert('Sorry, we could not submit your application. Please try again later.');
    } finally {
      document.getElementById('submitText').style.display = 'block';
      document.getElementById('spinner').style.display = 'none';
      btn.disabled = false;
    }
  }

  function showSuccess() {
    const overlay = document.getElementById('successOverlay');
    if (overlay) {
      overlay.classList.add('show');
      document.body.style.overflow = 'hidden';
      // Reset button
      document.getElementById('submitText').style.display = 'block';
      document.getElementById('spinner').style.display = 'none';
      document.getElementById('submitBtn').disabled = false;
      return;
    }
    alert('Submission successful.');
  }

  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', submitContactForm);
  }

  // Close overlay on backdrop click
  const successOverlay = document.getElementById('successOverlay');
  if (successOverlay) {
    successOverlay.addEventListener('click', function(e) {
      if (e.target === this) {
        this.classList.remove('show');
        document.body.style.overflow = '';
      }
    });
  });