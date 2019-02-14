// // Get the modal
// // var modal = document.getElementById('myModal');
// var modal = document.getElementsByClassName('modal');

// // Get the image and insert it inside the modal - use its "alt" text as a caption
// // var img = document.getElementById('myImg');
// var img = document.getElementsByClassName('myImg');
// var modalImg = document.getElementById("img01");
// var captionText = document.getElementById("caption");
// img.onclick = function(){
// 	alert("hi");
//   modal.style.display = "block";
//   modalImg.src = this.src;
//   captionText.innerHTML = this.alt;
// }

// // Get the <span> element that closes the modal
// var span = document.getElementsByClassName("close")[0];

// // When the user clicks on <span> (x), close the modal
// span.onclick = function() { 
//   modal.style.display = "none";
// }
// // When the user clicks anywhere outside of the modal, close it
// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// }

var img = document.getElementsByClassName('w3-hover-opacity');
img.onclick = function(){
	alert("hi");
}