
function dismissModal() {
    const form = document.getElementById('messageSentForm');
    const modal = bootstrap.Modal.getInstance(document.getElementById('connectModal'));
    form.reset();
    setTimeout(function(){
        modal.hide();
    }, 1000);
}


