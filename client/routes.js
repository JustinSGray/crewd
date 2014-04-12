Router.map(function() {
  this.route('home', {
    path: '/', 
    template: 'crewd', 
    layoutTemplate: 'layout' 
  }); 

  this.route('purchase', {
    path:'/purchase', 
    template:'purchase', 
    layoutTemplate: 'layout' 
  });
});