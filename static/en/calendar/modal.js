let modal = document.getElementById('eventModal');
let closeBtnFooter = document.getElementsByClassName('closeBtnFooter')[0];
let header = document.getElementById('modalHeader');

closeBtnFooter.addEventListener('click', closeModal);
window.addEventListener('click', clickOutside);

function closeModal() {
    modal.style.display = 'none';
    document.body.style.overflow = 'visible';
}

function clickOutside(e) {
    if (e.target == modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'visible';
    }
}

function loadmodal(newbutton) {
    var context = newbutton.getAttribute('context');
    var modal = document.getElementById('eventModal');
    var modalMain = document.getElementById('modalMain');
    var header = document.getElementById('modalHeader')
    var barHeader = newbutton.getAttribute('headerContext')
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        modalMain.innerHTML = context;
        header.innerHTML = barHeader;
    }
}
