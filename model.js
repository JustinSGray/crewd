Buys = new Meteor.Collection('buys'); 

Buys.allow({
  insert: function(userId, doc){return true;}, 
  update: function(userId, doc){return false;},
  remove: function(userId, doc){return false;}
});

Emails = new Meteor.Collection('emails');
Emails.allow({
  insert: function(userId, doc){
    var exists = Emails.findOne({addr: doc.addr}); 
    if (!exists) {  
      return true;
    }
  }, 
  update: function(userId, doc){return false;},
  remove: function(userId, doc){return false;}
});

