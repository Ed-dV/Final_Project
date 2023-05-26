const productImage = document.getElementById("product-image");
const zoomOverlay = document.createElement("div");
zoomOverlay.className = "zoom-overlay";
const zoomedImage = document.createElement("img");
zoomedImage.className = "zoomed-image";

var buttons = document.querySelectorAll(".btn-outline-primary");

productImage.addEventListener("mouseover", function() {
  if (!zoomOverlay.contains(zoomedImage)) {
    zoomedImage.src = productImage.src;
    zoomOverlay.appendChild(zoomedImage);
    document.body.appendChild(zoomOverlay);
  }
  zoomOverlay.style.display = "block";
});

zoomOverlay.addEventListener("mouseout", function() {
  zoomOverlay.style.display = "none";
  zoomOverlay.innerHTML = "";
});

function changeImage(event, imageUrl) {
  var productImage = document.getElementById('product-image');
  productImage.src = imageUrl;
}

  
  buttons.forEach(function(button) {
    button.addEventListener("click", function() {
      buttons.forEach(function(btn) {
        btn.classList.remove("active");
      });
      this.classList.add("active");
    });
  });
    function myFunction() {
    var popup = document.getElementById("myPopup");
    popup.classList.toggle("show");
  }
  

