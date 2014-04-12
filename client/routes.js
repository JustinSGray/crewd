Router.map(function() {
  this.route('home', {
    path: '/', 
    template: 'crewd', 
    layoutTemplate: 'layout',
    onBeforeAction: function(){
      Session.set('buyId', undefined);
    }
  }); 

  this.route('buy', {
    path:'/buy', 
    template:'buy', 
    layoutTemplate: 'layout', 
    waitOn: function(){
      return Meteor.subscribe('buys')
    }
  });
});