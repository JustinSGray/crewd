Template.crewd.events({
  'click .buy-app-button': function(event, template){

    var device = $(event.target).attr('device');

    var cb = function(error, buyId){
      Session.set('buyId', buyId);
      //console.log('Bought!', error ,buyId);
      Router.go('/buy');
    }
    //console.log(device)
    Buys.insert({device:device, price: 3}, cb);
    
  }
});