function openModal(imageUrl) {
    var modal = document.getElementById("imageModal");
    var modalImg = document.getElementById("modalImg");

    modal.style.display = "flex";  // show modal
    modalImg.src = imageUrl;  // set zoomed picture
}

function closeModal() {
    document.getElementById("imageModal").style.display = "none";
}
