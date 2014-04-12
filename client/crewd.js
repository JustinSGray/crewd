Template.crewd.events({
  'click .buy-app-button': function(event, template){

    var device = $(event.target).attr('device');


    Buys.insert({device:device, price: 3});
    Router.go('purhcase');
  }
});