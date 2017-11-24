$('.card-text').each(function(){
	var before = $(this).text();
	var search = $('#search').text();
	var after  = before.replace(search, ' <span style="background:#E2C2DE">'+ search +'</span> ');
	var search2 = search.substring(0,1).toUpperCase() + search.substring(1)
	var after2  = after.replace(search2, ' <span style="background:#E2C2DE">'+ search2 +'</span> ');
	$(this).html(after2);
});