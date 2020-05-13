function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
} 

$(document).ready(function(){
	$('.header__burger').click(function(event){
		$('.header__burger, .header__menu').toggleClass('active');
		$('body').toggleClass('lock');
	})
});


$(function(){
	$("#datetimepicker1").datetimepicker({
		format: 'DD/MM/YYYY HH:mm',
	});
});
