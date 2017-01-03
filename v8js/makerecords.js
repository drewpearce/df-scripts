function getCurrentRecordCount(endpoint) {
  var currentRecords = platform.api.get(endpoint + '?fields=id&limit=1&order=id%20DESC&include_count=true');

  if (currentRecords.content.resource.length > 0) {
    var currentOffset = parseInt(currentRecords.content.resource[0].id);
  } else {
    var currentOffset = 0;
  }

  return currentOffset;
}

function buildPayload(workingOffset) {
  var workingPayload = {"resource":[]};
  var xrecords = 0;

  if (event.request.parameters.xrecords) {
    xrecords = event.request.parameters.xrecords;
    if (workingOffset > 0) {
      xrecords = workingOffset + parseInt(xrecords);
    }
  } else {
    throw 'parameter xrecords is required';
  }

  for (var x=1 + workingOffset; x<=xrecords;x++) {
    var record = {};
    var completed = Math.floor(Math.random() * 2) + 0;
    record.name = "Todo Item " + x;
    record.complete = completed;
    workingPayload.resource.push(record);
  }

  return workingPayload;
}

var recordsEndpoint = 'db/_table/todo'; //Set the table where you want to created records
var offset = getCurrentRecordCount(recordsEndpoint);
var payload = buildPayload(offset);
var result = platform.api.post(recordsEndpoint, payload);
return result;
