$(function() {
	var timer=null;
	$("#username").hover(
	function()
	{clearTimeout(timer);
	 timer=setTimeout(function(){$(".org_box").css("display", "block");},300);
	},
	function(){
		clearTimeout(timer);
		timer=setTimeout(function(){$(".org_box").css("display", "none");},200);
	});
$(".org_box").hover(function(){$(".org_box").css("display", "block");},function(){$(".org_box").css("display", "none");})
})