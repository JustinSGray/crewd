Template.buy.events({
  'click #sign-up-submit': function(event, template){
    var email = $(event.target).parent().find('input[type=email]').val();
    var beta = $(event.target).parent().find('input[type=checkbox]').prop('checked');

    if(email) {
      Emails.insert({addr:email, beta:beta});
    }
  }
})