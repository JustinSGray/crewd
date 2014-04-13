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
      return Meteor.subscribe('buys');
    }
  });

  this.route('dashboard', {
    path: '/dashboard',
    template: 'dashboard',
    layoutTemplate: 'layout', 
    onBeforeAction: function(){
      if (Meteor.user()){
        Router.go('/buy');
      }
      else{
        Router.go('/');
      }
    },
  });

  this.route('thanks', {
    path:'/thanks', 
    template: 'thankyou', 
    layoutTemplate: 'layout', 
  });
});