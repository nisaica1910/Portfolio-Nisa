// ===== 0. Lompat ke section sesuai hash URL setelah layout settle =====
// (dibutuhkan karena body pakai CSS `zoom`, yang bikin lompatan hash
//  otomatis bawaan browser kadang salah hitung posisi)
window.addEventListener('load', () => {
  if (window.location.hash) {
    const target = document.querySelector(window.location.hash);
    if (target) {
      setTimeout(() => {
        target.scrollIntoView({ behavior: 'auto', block: 'start' });
      }, 50);
    }
  }
});

// ===== 1. Navbar: efek solid saat discroll =====
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('scrolled', window.scrollY > 10);
});

// ===== 2. Mobile menu toggle =====
const navToggle = document.getElementById('nav-toggle');
const navLinksWrap = document.getElementById('nav-links');

navToggle.addEventListener('click', () => {
  const isOpen = navLinksWrap.classList.toggle('open');
  navToggle.classList.toggle('open', isOpen);
  navToggle.setAttribute('aria-expanded', isOpen);
});

// Tutup menu mobile begitu salah satu link diklik
navLinksWrap.querySelectorAll('.nav-link').forEach((link) => {
  link.addEventListener('click', () => {
    navLinksWrap.classList.remove('open');
    navToggle.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
  });
});

// ===== 3. Scrollspy: highlight nav-link sesuai section yang kelihatan =====
const sections = document.querySelectorAll('main section[id]');
const navLinks = document.querySelectorAll('.nav-link');

const spyObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navLinks.forEach((link) => {
          link.classList.toggle('active', link.dataset.section === id);
        });
      }
    });
  },
  { rootMargin: '-45% 0px -50% 0px', threshold: 0 }
);
sections.forEach((section) => spyObserver.observe(section));

// ===== 4. Modal detail project =====
document.querySelectorAll('[data-modal-trigger]').forEach((card) => {
  card.addEventListener('click', () => {
    const modal = document.getElementById(card.dataset.modalTrigger);
    if (modal) modal.classList.add('open');
  });
});
document.querySelectorAll('[data-modal-close]').forEach((btn) => {
  btn.addEventListener('click', () => {
    btn.closest('.modal')?.classList.remove('open');
  });
});
document.querySelectorAll('.modal').forEach((modal) => {
  modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.classList.remove('open');
  });
});

// ===== 5. Lightbox untuk foto organisasi & sertifikat =====
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');
const lightboxCaption = document.getElementById('lightbox-caption');

document.querySelectorAll('[data-lightbox-src]').forEach((el) => {
  el.addEventListener('click', () => {
    lightboxImg.src = el.dataset.lightboxSrc;
    lightboxCaption.textContent = el.dataset.lightboxCaption || '';
    lightbox.classList.add('open');
  });
});
document.querySelectorAll('[data-lightbox-close]').forEach((btn) => {
  btn.addEventListener('click', () => lightbox.classList.remove('open'));
});
lightbox.addEventListener('click', (e) => {
  if (e.target === lightbox) lightbox.classList.remove('open');
});

// ===== 5b. Show more/less untuk daftar Event =====
const eventsList = document.getElementById('events-list');
const eventsToggle = document.getElementById('events-toggle');
const EVENTS_VISIBLE_COUNT = 3;

if (eventsList && eventsToggle) {
  const eventItems = Array.from(eventsList.querySelectorAll('.org-entry'));
  const extraEvents = eventItems.slice(EVENTS_VISIBLE_COUNT);

  if (extraEvents.length > 0) {
    extraEvents.forEach((item) => item.classList.add('timeline-hidden'));

    eventsToggle.addEventListener('click', () => {
      const isExpanded = eventsToggle.dataset.expanded === 'true';
      extraEvents.forEach((item) => item.classList.toggle('timeline-hidden', isExpanded));
      eventsToggle.dataset.expanded = String(!isExpanded);
      eventsToggle.textContent = isExpanded ? eventsToggle.dataset.show : eventsToggle.dataset.hide;
    });
  } else {
    eventsToggle.style.display = 'none';
  }
}

// ===== 6. Toggle bahasa tetap di posisi scroll yang sama =====

// Begitu halaman dibuka, cek apakah ada posisi scroll yang dititipkan
// lewat URL (?scrollY=....), lalu lompat ke situ dan bersihkan URL-nya.
(function restoreScrollPosition() {
  const params = new URLSearchParams(window.location.search);
  const y = params.get('scrollY');
  if (y !== null) {
    window.scrollTo(0, parseInt(y, 10) || 0);
    params.delete('scrollY');
    const newSearch = params.toString();
    const newUrl = window.location.pathname + (newSearch ? '?' + newSearch : '');
    history.replaceState(null, '', newUrl);
  }
})();

document.querySelectorAll('.lang-option').forEach((link) => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const url = new URL(link.href, window.location.origin);
    url.searchParams.set('scrollY', Math.round(window.scrollY));
    window.location.href = url.pathname + url.search;
  });
});

// ===== 7. Tutup modal/lightbox pakai tombol Escape =====
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal.open').forEach((m) => m.classList.remove('open'));
    lightbox.classList.remove('open');
  }
});

// ===== Tab skills di section About =====
document.querySelectorAll('[data-skills-tab]').forEach((tab) => {
  tab.addEventListener('click', () => {
    const target = tab.dataset.skillsTab;
    document.querySelectorAll('[data-skills-tab]').forEach((t) => t.classList.toggle('active', t === tab));
    document.querySelectorAll('[data-skills-pane]').forEach((pane) => {
      pane.classList.toggle('active', pane.dataset.skillsPane === target);
    });
  });
});