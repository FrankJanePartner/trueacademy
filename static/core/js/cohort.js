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

//NAVBAR END

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => {
        entry.target.classList.add("visible");
      }, i * 80);
    }
  });
}, {
  threshold: 0.1,
  rootMargin: "0px 0px -40px 0px"
});

document.querySelectorAll(".fade-up").forEach((el) => {
  observer.observe(el);
});