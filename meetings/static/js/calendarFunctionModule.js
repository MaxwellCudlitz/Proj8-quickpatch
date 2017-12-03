var initializeHandles = function()
{
  // update all calendar buttons
  updateCalendars();

  // listen for calendar button presses- on button press,
  // synchronize with flask session state
  $('.calButton').click(function()
  {
    toggleCalendar(this.id);
  });
};

//////
// module exposing a function that updates the
// renders for which buttons are and are not toggled,
// loaded from the user's flask session
//////
var getFreeBusy = function()
{
  callAJAX('GET', '/api/_freebusy', null,
    function(res){
      var calRes = JSON.parse(res['responseText']);
      renderEvents(calRes);
    });
};

//////
// module exposing a function that updates the
// renders for which buttons are and are not toggled,
// loaded from the user's flask session
//////
var updateCalendars = function()
{
  callAJAX('GET', '/api/_selectedcals', null, renderToggledButtons);
};

//////
// module exposing calendar toggling functionality
//////
var toggleCalendar = function(id)
{
  callAJAX('POST', '../api/session/_togglecal', 
    JSON.stringify({'id' : id}), renderToggledButtons);
};

//////
// makes an ajax call with the passed prams
//////
var callAJAX = function(type, url, dat, resCallback)
{
  $.ajax(
  {
    type : type,
    url : url,
    data : dat,
    contentType: 'application/json; charset=utf-8'
  })
  .complete(function(res)
  {
    if(resCallback) 
    {
      resCallback(res);
    }
  });
}

//////
// Renders all events during timeframe
/////
var renderEvents = function(events)
{
  console.log(events);
  console.log("trying to render");

  // template for individual event
  const eventTemplate = (cal, start, end, message) => 
  `
    <div class="form-control form-rounded col-4">
      <div class="panel-heading">${message}</div>
      <div class="panel-body">${start} - ${end}</div>
    </div>
  `

  // format events
  var renderedEventList = [];
  for(i in events){
      // reverse order iteration without flipping list
      var event = events[events.length - i - 1];

      // localize times
      var start = toLocalTime(event['start']);
      var end   = toLocalTime(event['end']);

      // message
      var msg = event['busy'] ? 'busy' : 'free';

      renderedEventList.push(
        eventTemplate(event['cal'], start, end, msg)
      );
  }

  // render events
  $('#busy_list').html(
    renderedEventList.join('')
  );

  // colorize forms
  colorizeEvents($('#busy_list'));
}

//////
// converts a UTC string to local time, if it is able to be parsed
//////
var toLocalTime = function(isoStr)
{
  // validate isostring
  if(moment(isoStr).isValid())
  {
    // this one has a prettier print.
    // return moment(isoStr).local();
    return moment(isoStr).local().format('YYYY-DD-MM HH:mm:ss');
  }
    
  console.log("tried to parse invalid date" + isoStr);
  return isoStr;
}

// TODO: this is still being troublesome. BootStrap CSS does not seem
// to want to be properly overloaded. At this time, this is just a reminder
// for future functionality.
var colorizeEvents = function(htmlParent)
{
  console.log("Reminder; add colorize module functionality in later iteration- probably final project");
  // htmlParent.each(function(){
  // });
}

//////
// updates all button's renders to the server's button state
//
// on a button render, freebusy will be queried.
//////
var renderToggledButtons = function(res)
{
  calRes = JSON.parse(res['responseText']);

  ids = calRes['cals'];

  // clear all buttons
  clearButtonRender();

  console.log(ids);
  // render active ones
  for(i in ids){
    renderButton(ids[i], 'active');
  }

  getFreeBusy();
};

//////
// clear all actively toggled buttons
//////
var clearButtonRender = function()
{
  $('.calButton').each(function(){
    renderButton(this.id, 'inactive');
  });
};

//////
// renders the current button as either
// active or inactive by changing it's
// state
//////
var renderButton = function(buttonId, state)
{
  var elem = $(document.getElementById(buttonId));
  if(state === 'active'){
    elem.addClass('active');
  }
  else{
    elem.removeClass('active');
  }
};