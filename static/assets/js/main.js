const menuToggle = document.getElementById('mobile-menu-open');
const menuContainer = document.getElementById('mobile-menu');
const menuContainerOverlay = document.getElementById('menu-overlay');
let navMainMenu = document.querySelectorAll('#nav-main-menu li')

menuToggle.addEventListener('click', () => {
  menuContainer.classList.toggle('hidden');
  menuContainerOverlay.classList.toggle('hidden')

 menuContainer.setAttribute('menu-visible', 'true')
 menuToggle.setAttribute('aria-expanded', 'true');
});
//
menuContainerOverlay.addEventListener('click', ()=> {
  menuContainer.classList.toggle('hidden');
  menuContainerOverlay.classList.toggle('hidden')

  menuContainer.setAttribute('menu-visible', 'false')
  menuToggle.setAttribute('aria-expanded', 'false');
});

// Add aria-expanded to nav-main-menu items on mouseenter and mouseleave
navMainMenu.forEach(function(item) {
  item.addEventListener('mouseenter', () => {
    item.setAttribute('aria-expanded', 'true');
  });
  item.addEventListener('mouseleave', () => {
    item.setAttribute('aria-expanded', 'false');
  })
})