Router.map(function() {
  this.route('home', {
    path: '/', 
    template: 'crewd', 
    layoutTemplate: 'layout',
    onBeforeAction: function(){
      if (Meteor.user()){
        Router.go('/dashboard');
      }
      Session.set('buyId', undefined);
    }
  }); 

  this.route('buy', {
    path:'/buy', 
    template:'buy', 
    layoutTemplate: 'layout', 
    onBeforeAction: function(){
      if (Meteor.user()){
        Router.go('/dashboard');
      }
    },
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
        Router.go('/dashboard');
      }
    },
  });
});