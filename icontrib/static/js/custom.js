$(document).ready(function() {
  $('#fullpage').fullpage({
		// anchors: ['hello', 'hashtag', 'goal', 'payment', 'done']
		anchors: ['step-hello','step-campaign','step-goal', 'step-payment'],
		sectionsColor: ['whitesmoke', '#1bbc9b', '#4BBFC3', '#7BAABE'],
		scrollingSpeed : 500,
		menu : '#menu'
	});
	var hashtag = document.getElementById('campaignField');
  if (hashtag) {
    hashtag.addEventListener('keyup', hashtagEventListener);
  }
	var goalField = document.getElementById('goalAmountField');
  if (goalField) {
  	goalField.addEventListener('keyup', goalEventListener);
  }
	var contribField = document.getElementById('contribAmountField');
  if (contribField) {
    contribField.addEventListener('keyup', contribEventListener);
  }
});




// Map [Enter] key to work like the [Tab] key
// Daniel P. Clark 2014

// Catch the keydown for the entire document
$(document).keydown(function(e) {

  // Set self as the current item in focus
  var self = $(':focus'),
      // Set the form by the current item in focus
      form = self.parents('form:eq(0)'),
      focusable;

  // Array of Indexable/Tab-able items
  focusable = form.find('input,a,select,button,textarea,div[contenteditable=true]').filter(':visible');

  function enterKey(){
    if (e.which === 13 && !self.is('textarea,div[contenteditable=true]')) { // [Enter] key

      // If not a regular hyperlink/button/textarea
      if ($.inArray(self, focusable) && (!self.is('a,button'))){
        // Then prevent the default [Enter] key behaviour from submitting the form
        e.preventDefault();
      } // Otherwise follow the link/button as by design, or put new line in textarea

      // Focus on the next item (either previous or next depending on shift)
      focusable.eq(focusable.index(self) + (e.shiftKey ? -1 : 1)).focus();

      return false;
    }
  }
  // We need to capture the [Shift] key and check the [Enter] key either way.
  if (e.shiftKey) { enterKey() } else { enterKey() }
});

$( ".target" ).change(function() {
})

// fullpage.initialize('#fullpage', {
// 	anchors: ['hello', 'hashtag', 'goal', 'payment', 'done'],
// 	menu: '#menu',
// 	css3:false
// });

function  hashtagEventListener() {
	var hashtag = document.getElementById('hashtagfield');
    new_value = hashtag.value.replace(/[^\w\s]/gi, '');
    new_value = '#'+new_value;
	hashtag.value = new_value

}

function  goalEventListener() {
	var cost = document.getElementById('goalAmountField');
    new_value = cost.value.replace(/[^0-9.]/gi, '');
    new_value = '$'+new_value;
	cost.value = new_value
}

function  contribEventListener() {
	var cost = document.getElementById('contribAmountField');
    new_value = cost.value.replace(/[^0-9.]/gi, '');
    new_value = '$'+new_value;
	cost.value = new_value
}

