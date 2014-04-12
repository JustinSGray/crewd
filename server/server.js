Meteor.publish('buys', function(){
  return Buys.find();
})