
function QueryValidator()
{
// bind a simple alert window to this controller to display any errors //
	this.queryErrors = $('.modal-alert');
	this.showQueryError = function(t, m)
	{
		$('.modal-alert .modal-header h4').text(t);
		$('.modal-alert .modal-body').html(m);
		this.queryErrors.modal('show');
	}
}

QueryValidator.prototype.validateForm = function()
{
	if ($('#user_input').val() == ''){
		this.showQueryError('Whoops!', 'Please enter a word');
		return false;
	} else {
		return true;
	}
}

$(document).ready(function(){
	var qv = new QueryValidator();
// main query form //
	$('#query .btn.btn-success').click(function(){ 
		var isCorrect = qv.validateForm();
		if (isCorrect == false) {
			return false;
		}
	});
	$('#user_input').focus();
});