window.addEventListener('scroll', () => {
    const nav = document.getElementsByTagName('nav')[0];
    var companyName = document.getElementById('company-name');
    var search = document.getElementById('search')
    const scrollDirection = window.scrollY;
    
    if (scrollDirection > 50) {
        nav.classList.add('scrolled');
        companyName.style.color='white';
        search.style.border='0.9px solid black';
    } else {
      
            nav.classList.remove('scrolled');
      
        companyName.style.color='rgb(138, 198, 74)';
        search.style.border='0.8px solid white'

    }
});
