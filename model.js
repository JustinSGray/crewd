Buys = new Meteor.Collection('buys'); 

Buys.allow({
  insert: function(doc, userId){return true;}, 
  update: function(doc, userId){return false;},
  remove: function(doc, userId){return false;}
});

Emails = new Meteor.Collection('emails');
Emails.allow({
  insert: function(doc, userId){
    var exists = Email.findOne({addr: doc.addr}); 
    if (!exists) {  
      return true;
    }
  }, 
  update: function(doc, userId){return false;},
  remove: function(doc, userId){return false;}
});

