/*=============== SHOW MENU ===============*/
const showMenu = (toggleId, navId) => {
    const toggle = document.getElementById(toggleId);
    const nav = document.getElementById(navId);

    toggle.addEventListener('click', () => {
        nav.classList.toggle('show-menu');
        toggle.classList.toggle('show-icon');
    });
};

/*=============== SHOW DROPDOWN MENU ===============*/
const dropdownItems = document.querySelectorAll('.dropdown__item');

dropdownItems.forEach(item => {
    const dropdownButton = item.querySelector('.dropdown__button');

    dropdownButton.addEventListener('click', () => {
        toggleItem(item);
    });
});

// Function to toggle dropdown visibility
const toggleItem = (item) => {
    const dropdownContainer = item.querySelector('.dropdown__container');
    const isActive = item.classList.contains('show-dropdown');

    dropdownItems.forEach(otherItem => {
        if (otherItem !== item) {
            closeDropdown(otherItem);
        }
    });

    if (isActive) {
        closeDropdown(item);
    } else {
        openDropdown(item);
    }
};

// Function to open dropdown
const openDropdown = (item) => {
    const dropdownContainer = item.querySelector('.dropdown__container');
    dropdownContainer.style.height = dropdownContainer.scrollHeight + 'px';
    item.classList.add('show-dropdown');
};

// Function to close dropdown
const closeDropdown = (item) => {
    const dropdownContainer = item.querySelector('.dropdown__container');
    dropdownContainer.removeAttribute('style');
    item.classList.remove('show-dropdown');
};

/*=============== DELETE DROPDOWN STYLES ===============*/
const mediaQuery = matchMedia('(min-width: 1118px)');
const dropdownContainers = document.querySelectorAll('.dropdown__container');

// Function to remove dropdown styles in desktop mode when browser resizes
const removeStyle = () => {
    if (mediaQuery.matches) {
        dropdownContainers.forEach(container => {
            container.removeAttribute('style');
        });

        dropdownItems.forEach(item => {
            item.classList.remove('show-dropdown');
        });
    }
};

addEventListener('resize', removeStyle);

// Initialize menu toggle and dropdown functionality
showMenu('nav-toggle', 'nav-menu');
dropdownItems.forEach(item => {
    item.addEventListener('click', function() {
        this.classList.toggle('active');
    });
});

/*=============== TOGGLE DARK MODE ===============*/
// main.js

function toggleDarkMode() {
    var element = document.body;
    element.classList.toggle("dark-mode");
  
    var darkModeToggle = document.getElementById('dark-mode-toggle');
    if (element.classList.contains("dark-mode")) {
      darkModeToggle.textContent = "Light Mode"; // Change text to Light Mode
    } else {
      darkModeToggle.textContent = "Dark Mode"; // Change text to Dark Mode
    }
  }
    // Toggle Menu
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        navToggle.querySelector('.ri-menu-line').classList.toggle('hide');
        navToggle.querySelector('.ri-close-line').classList.toggle('show');
    });

   

    // Call the function to display random numbers when the page loads
    window.onload = displayRandomNumbers;
    