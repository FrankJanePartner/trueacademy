//NAVBAR START
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
// NAVBAR END

// GALLERY PICTURES START
// NAVBAR START
  function toggleMenu() {
    document.getElementById('mobileMenu').classList.toggle('active');
  }
// NAVBAR END

// GALLERY START
// ================= DATA =================
const galleryData = {
  2025: [
    { src: "asset/workshops-1.jpg" },
    { src: "asset/workshops-2.jpg" },
    { src: "asset/workshops-3.jpg" },
    { src: "asset/workshops-4.jpg" },
    { src: "asset/workshops-5.jpg" },
    { src: "asset/workshops-6.jpg" },
    { src: "asset/workshops-7.jpg" },
    { src: "asset/graduation-1.jpg" },
    { src: "asset/graduation-2.jpg" },
    { src: "asset/graduation-3.jpg" },
    { src: "asset/graduation-4.jpg" },
  ],

  2024: [
    { src: "asset/workshops-1.jpg" },
    { src: "asset/workshops-2.jpg" },
    { src: "asset/workshops-3.jpg" },
    { src: "asset/workshops-4.jpg" },
    { src: "asset/workshops-5.jpg" },
    { src: "asset/workshops-6.jpg" },
    { src: "asset/workshops-7.jpg" },

  ],

  2023: [
    { src: "asset/graduation-1.jpg" },
    { src: "asset/graduation-2.jpg" },
    { src: "asset/graduation-3.jpg" },
    { src: "asset/graduation-4.jpg" },
    { src: "asset/graduation-5.jpg" },
    { src: "asset/graduation-6.jpg" },
    { src: "asset/graduation-7.jpg" },
    { src: "asset/graduation-8.jpg" },
  ]
};

// ================= STATE =================
let currentImages = [];
let currentIndex = 0;
let slideInterval;
let selectedImages = [];

// ================= RENDER =================
function renderGallery(year) {
  const grid = document.getElementById("galleryGrid");
  const title = document.getElementById("galleryTitle");

  const images = galleryData[year];
  currentImages = images;

  grid.innerHTML = "";
//   title.innerText = `Light Camp ${year}`;

  images.forEach((img, index) => {

    const div = document.createElement("div");

    div.className = "break-inside-avoid relative group cursor-pointer overflow-hidden rounded-xl";

    div.innerHTML = `
      <img src="${img.src}" loading="lazy"
        class="w-full rounded-xl transition duration-500 group-hover:scale-105 group-hover:brightness-75">

      <!-- DARK HOVER -->
      <div class="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition"></div>

      <!-- ZOOM ICON -->
      <svg class="w-5 h-5 absolute top-3 right-3 opacity-0 group-hover:opacity-100 text-white transition"
        fill="none" stroke="currentColor">
        <circle cx="11" cy="11" r="8" stroke-width="2"/>
        <path d="M21 21l-4.3-4.3" stroke-width="2"/>
      </svg>

      <!-- SELECT BUTTON -->
      <button class="select-btn absolute top-3 left-3 bg-white/80 text-[#173b70] rounded-full w-7 h-7 flex items-center justify-center"
        onclick="selectImage(event, '${img.src}')">

        <svg class="w-4 h-4" fill="none" stroke="currentColor">
          <path stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>

      </button>
    `;

    // div.onclick = (e) => {
    //   if (e.target.closest(".select-btn")) return;
    //   openLightbox(index);
    // };

    div.onclick = () => {
  selectImage(null, img.src);
};

    grid.appendChild(div);
  });
}

// ================= LIGHTBOX =================
function openLightbox(index) {
  currentIndex = index;
  showSlide();
  document.getElementById("lightbox").classList.remove("hidden");
}

function closeLightbox() {
  document.getElementById("lightbox").classList.add("hidden");
}

function showSlide() {
  const img = currentImages[currentIndex];
  document.getElementById("lightboxImg").src = img.src;
}

// ================= SELECT =================
function selectImage(e, src) {
  e.stopPropagation();

  if (selectedImages.includes(src)) return;

  selectedImages.push(src);
  renderSelected();
}

// ================= RENDER SELECTED =================
function renderSelected() {
  const container = document.getElementById("selectedContainer");
  container.innerHTML = "";

  selectedImages.forEach(src => {

    const div = document.createElement("div");
    div.className = "relative";

    div.innerHTML = `
      <img src="${src}" class="w-20 h-20 object-cover rounded-lg">

      <button onclick="removeImage('${src}')"
        class="absolute -top-2 -right-2 bg-red-600 text-white rounded-full w-5 h-5 flex items-center justify-center">

        <svg class="w-3 h-3" fill="none" stroke="currentColor">
          <path stroke-width="2" d="M6 6l12 12M6 18L18 6"/>
        </svg>

      </button>
    `;

    container.appendChild(div);
  });
}

// ================= REMOVE =================
function removeImage(src) {
  selectedImages = selectedImages.filter(img => img !== src);
  renderSelected();
}

// ================= FILTER =================
function filterYear(year, btn) {
  renderGallery(year);

  document.querySelectorAll(".year-btn").forEach(b => {
    b.classList.remove("bg-[#173b70]","text-white");
    b.classList.add("bg-[#173b70]","text-white-600");
  });

  btn.classList.add("bg-[#173b70]","text-white");
}

// ================= INIT =================
renderGallery(2025);

//GALLERY END
// GALLERY PICTURES END