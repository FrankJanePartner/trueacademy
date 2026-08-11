// ── Navbar ────────────────────────────────────────────────────────────────────
const navbar    = document.getElementById('navbar');
const menuBtn   = document.getElementById('menuBtn');
const mobileMenu = document.getElementById('mobileMenu');
const menuIcon  = document.getElementById('menuIcon');

window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 8);
});

menuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('show');
    menuIcon.innerHTML = mobileMenu.classList.contains('show') ? '&times;' : '&#9776;';
});

document.querySelectorAll('.mobile-menu a').forEach(link => {
    link.addEventListener('click', () => {
        mobileMenu.classList.remove('show');
        menuIcon.innerHTML = '&#9776;';
    });
});

document.querySelectorAll('.desktop-nav a, .mobile-menu a').forEach(link => {
    if (link.href === window.location.href) link.classList.add('active');
});
// ── End Navbar ────────────────────────────────────────────────────────────────


// ── Gallery state ─────────────────────────────────────────────────────────────
let allGalleryImages = [];
let currentCategorySlug = 'all';
const API_REQUEST_TIMEOUT_MS = 15000;
const IMAGE_PLACEHOLDER_URL = '/static/core/asset/hero.png';

async function fetchGalleryJson(url) {
    const controller = new AbortController();
    const timeoutId = window.setTimeout(() => controller.abort(), API_REQUEST_TIMEOUT_MS);

    try {
        const response = await fetch(url, { signal: controller.signal });
        if (!response.ok) throw new Error(`Request returned ${response.status}`);
        return await response.json();
    } finally {
        window.clearTimeout(timeoutId);
    }
}

// ── Fetch + render categories ─────────────────────────────────────────────────
async function fetchCategories() {
    const container = document.getElementById('categoryFilters');
    if (!container) return;

    try {
        const categories = await fetchGalleryJson('/api/gallery/categories/');

        // Build dynamic buttons
        container.innerHTML = '';

        // ALL button (active by default)
        const allBtn = document.createElement('button');
        allBtn.className = 'cat-btn bg-[#173b70] text-white px-5 py-2 rounded-full text-sm font-medium transition shadow-sm';
        allBtn.textContent = 'ALL';
        allBtn.onclick = () => filterCategory('all', allBtn);
        container.appendChild(allBtn);

        categories.forEach(cat => {
            const btn = document.createElement('button');
            btn.className = 'cat-btn bg-white text-gray-700 hover:bg-[#173b70] hover:text-white px-5 py-2 rounded-full text-sm font-medium transition shadow-sm';
            btn.textContent = cat.name.toUpperCase();
            btn.dataset.slug = cat.slug;
            btn.onclick = () => filterCategory(cat.slug, btn);
            container.appendChild(btn);
        });
    } catch (err) {
        console.error('Could not load gallery categories:', err);
        // The gallery data remains API-only; keep just the universal filter available.
        container.innerHTML = '';
        const allBtn = document.createElement('button');
        allBtn.className = 'cat-btn bg-[#173b70] text-white px-5 py-2 rounded-full text-sm font-medium transition shadow-sm';
        allBtn.textContent = 'ALL';
        allBtn.onclick = () => filterCategory('all', allBtn);
        container.appendChild(allBtn);

        const message = document.createElement('span');
        message.className = 'w-full text-xs text-gray-400';
        message.textContent = 'Categories could not be loaded. Showing all images.';
        container.appendChild(message);
    }
}

// ── Fetch + render gallery images ─────────────────────────────────────────────
async function fetchGalleryImages() {
    const grid = document.getElementById('galleryGrid');
    if (!grid) return;

    grid.innerHTML = `
        <div class="col-span-full py-16 text-center text-gray-400">
            <svg class="mx-auto mb-3 w-8 h-8 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
            </svg>
            <p class="text-sm">Loading gallery...</p>
        </div>`;

    try {
        const data = await fetchGalleryJson('/api/gallery/');

        if (!Array.isArray(data) || data.length === 0) {
            grid.innerHTML = `
                <div class="col-span-full py-16 text-center text-gray-500 font-medium">
                    No gallery images have been added yet.
                </div>`;
            return;
        }

        allGalleryImages = data;
        renderGallery();
    } catch (err) {
        console.error('Gallery API error:', err);
        grid.innerHTML = `
            <div class="col-span-full py-16 text-center text-gray-500">
                <p class="font-semibold text-red-500 mb-2">Could not load gallery images.</p>
                <p class="text-sm">Please check your connection and try refreshing the page.</p>
            </div>`;
    }
}

// ── Render filtered images ────────────────────────────────────────────────────
function renderGallery() {
    const grid = document.getElementById('galleryGrid');
    if (!grid) return;

    grid.innerHTML = '';

    const filtered = currentCategorySlug === 'all'
        ? allGalleryImages
        : allGalleryImages.filter(img => {
            const slug = img.category?.slug || img.category || '';
            return slug.toLowerCase() === currentCategorySlug.toLowerCase();
        });

    if (filtered.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full py-12 text-center text-gray-500 font-medium">
                No images found in this category.
            </div>`;
        return;
    }

    filtered.forEach(img => {
        const div = document.createElement('div');
        div.className = 'break-inside-avoid relative group cursor-pointer overflow-hidden rounded-xl bg-gray-200 mb-4 shadow-sm hover:shadow-lg transition duration-300';

        // category may be a nested object (from API) or a string (legacy)
        const catName  = img.category?.name  || (typeof img.category === 'string' ? img.category : 'Other');
        const titleText = img.title || 'Trinity Real Estate University';
        const imageUrl  = img.image_url || '';

        div.innerHTML = `
            <img
                src="${IMAGE_PLACEHOLDER_URL}"
                loading="lazy"
                decoding="async"
                alt="${titleText}"
                onerror="this.onerror=null; this.src='${IMAGE_PLACEHOLDER_URL}';"
                class="w-full rounded-xl transition duration-500 group-hover:scale-105 group-hover:brightness-90 object-cover">

            <!-- Hover overlay -->
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent
                        opacity-0 group-hover:opacity-100 transition duration-300
                        flex flex-col justify-between p-3 text-white">
                <div class="flex justify-between items-start">
                    <span class="bg-yellow-400 text-gray-900 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">
                        ${catName}
                    </span>
                    <span class="text-xs font-semibold text-gray-200 bg-black/40 px-2 py-0.5 rounded-md">
                        ${img.year || ''}
                    </span>
                </div>
                <div>
                    <h4 class="text-sm font-semibold truncate">${titleText}</h4>
                </div>
            </div>`;

        // Do not expose a browser broken-image icon while the media file is loading.
        // The API image URL remains the source of truth and replaces this placeholder on load.
        if (imageUrl) {
            const displayedImage = div.querySelector('img');
            const preloadedImage = new Image();
            preloadedImage.onload = () => {
                displayedImage.src = imageUrl;
            };
            preloadedImage.src = imageUrl;
        }

        div.onclick = () => openLightbox(img);
        grid.appendChild(div);
    });
}

// ── Category filter ───────────────────────────────────────────────────────────
function filterCategory(slug, btn) {
    currentCategorySlug = slug;

    document.querySelectorAll('.cat-btn').forEach(b => {
        b.classList.remove('bg-[#173b70]', 'text-white');
        b.classList.add('bg-white', 'text-gray-700');
    });
    if (btn) {
        btn.classList.remove('bg-white', 'text-gray-700');
        btn.classList.add('bg-[#173b70]', 'text-white');
    }

    renderGallery();
}

// ── Lightbox ──────────────────────────────────────────────────────────────────
function openLightbox(img) {
    const lightbox     = document.getElementById('lightbox');
    const lightboxImg  = document.getElementById('lightboxImg');
    const lightboxTitle = document.getElementById('lightboxTitle');
    const lightboxBadge = document.getElementById('lightboxBadge');
    if (!lightbox) return;

    const catName = img.category?.name || (typeof img.category === 'string' ? img.category : 'Other');

    if (lightboxImg) {
        lightboxImg.src = img.image_url || '';
        lightboxImg.onerror = function () {
            this.onerror = null;
            this.src = '/static/core/asset/hero.png';
        };
    }
    if (lightboxTitle) lightboxTitle.textContent = img.title || 'Campus Moment';
    if (lightboxBadge) lightboxBadge.textContent = `${catName.toUpperCase()} · ${img.year || ''}`;

    lightbox.classList.remove('hidden');
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    if (lightbox) lightbox.classList.add('hidden');
}

// Close lightbox on Escape key
document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeLightbox();
});

// ── Bootstrap ─────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    fetchCategories();
    fetchGalleryImages();
});
