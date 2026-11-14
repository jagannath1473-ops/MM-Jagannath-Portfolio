const header = document.querySelector('[data-header]');
const menuToggle = document.querySelector('[data-menu-toggle]');
const navLinks = document.querySelector('[data-nav-links]');
const scrollProgress = document.querySelector('[data-scroll-progress]');
const cursorAura = document.querySelector('[data-cursor-aura]');
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const updateHeader = () => {
  header.classList.toggle('scrolled', window.scrollY > 20);
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;
  const progress = scrollable > 0 ? window.scrollY / scrollable : 0;
  scrollProgress.style.transform = `scaleX(${Math.min(1, Math.max(0, progress))})`;
};
updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });

menuToggle.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', String(isOpen));
});

navLinks.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    menuToggle.setAttribute('aria-expanded', 'false');
  });
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((element) => revealObserver.observe(element));

if (!prefersReducedMotion) {
  let auraX = window.innerWidth / 2;
  let auraY = window.innerHeight / 2;
  let auraFrame = 0;

  window.addEventListener('pointermove', (event) => {
    auraX = event.clientX;
    auraY = event.clientY;
    if (!auraFrame) {
      auraFrame = requestAnimationFrame(() => {
        cursorAura.style.transform = `translate3d(${auraX}px, ${auraY}px, 0)`;
        auraFrame = 0;
      });
    }
  }, { passive: true });

  const parallaxItems = document.querySelectorAll('[data-parallax]');
  let parallaxFrame = 0;
  const updateParallax = () => {
    parallaxItems.forEach((item) => {
      const rect = item.getBoundingClientRect();
      const offset = (rect.top + rect.height / 2 - window.innerHeight / 2) / window.innerHeight;
      const strength = Number(item.dataset.parallax || 0);
      item.style.transform = `translate3d(0, ${offset * strength}px, 0)`;
    });
    parallaxFrame = 0;
  };
  window.addEventListener('scroll', () => {
    if (!parallaxFrame) parallaxFrame = requestAnimationFrame(updateParallax);
  }, { passive: true });
  updateParallax();

  document.querySelectorAll('[data-tilt]').forEach((card) => {
    card.addEventListener('pointermove', (event) => {
      const rect = card.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width;
      const y = (event.clientY - rect.top) / rect.height;
      card.style.setProperty('--tilt-x', `${(x - 0.5) * 5}deg`);
      card.style.setProperty('--tilt-y', `${(0.5 - y) * 5}deg`);
      card.style.setProperty('--spot-x', `${x * 100}%`);
      card.style.setProperty('--spot-y', `${y * 100}%`);
    });
    card.addEventListener('pointerleave', () => {
      card.style.setProperty('--tilt-x', '0deg');
      card.style.setProperty('--tilt-y', '0deg');
    });
  });

  document.querySelectorAll('[data-spotlight]').forEach((element) => {
    element.addEventListener('pointermove', (event) => {
      const rect = element.getBoundingClientRect();
      element.style.setProperty('--spot-x', `${event.clientX - rect.left}px`);
      element.style.setProperty('--spot-y', `${event.clientY - rect.top}px`);
    });
  });
}

const sections = document.querySelectorAll('main section[id]');
const navigationAnchors = document.querySelectorAll('.nav-links a[href^="#"]');
const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      navigationAnchors.forEach((anchor) => {
        anchor.classList.toggle('active', anchor.getAttribute('href') === `#${entry.target.id}`);
      });
    }
  });
}, { rootMargin: '-38% 0px -52%', threshold: 0 });
sections.forEach((section) => sectionObserver.observe(section));

const form = document.getElementById('contact-form');
const statusBox = document.getElementById('form-status');
const submitButton = form.querySelector('button[type="submit"]');
const messageInput = document.getElementById('message');
const messageCount = document.getElementById('message-count');

messageInput.addEventListener('input', () => {
  messageCount.textContent = messageInput.value.length;
});

const clearErrors = () => {
  form.querySelectorAll('.field-error').forEach((element) => { element.textContent = ''; });
  form.querySelectorAll('.invalid').forEach((element) => element.classList.remove('invalid'));
  statusBox.className = 'form-status';
  statusBox.textContent = '';
};

const showErrors = (errors = {}) => {
  Object.entries(errors).forEach(([field, error]) => {
    const input = document.getElementById(field);
    const errorBox = document.getElementById(`${field}-error`);
    if (input && errorBox) {
      input.classList.add('invalid');
      input.setAttribute('aria-invalid', 'true');
      input.setAttribute('aria-describedby', `${field}-error`);
      errorBox.textContent = error;
    }
  });
};

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  clearErrors();
  submitButton.disabled = true;
  submitButton.classList.add('loading');

  const payload = {
    name: form.elements.name.value.trim(),
    email: form.elements.email.value.trim(),
    message: form.elements.message.value.trim(),
  };

  try {
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(payload),
    });
    const result = await response.json();
    if (!response.ok) {
      showErrors(result.errors);
      throw new Error(result.message || 'Your message could not be submitted.');
    }
    statusBox.className = 'form-status success';
    statusBox.textContent = result.message;
    form.reset();
    messageCount.textContent = '0';
  } catch (error) {
    statusBox.className = 'form-status error';
    statusBox.textContent = error.message || 'The server is unavailable. Please try again.';
  } finally {
    submitButton.disabled = false;
    submitButton.classList.remove('loading');
  }
});

document.getElementById('current-year').textContent = new Date().getFullYear();
