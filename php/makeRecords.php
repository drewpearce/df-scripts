<?php

$api = $platform['api'];
$get = $api->get;
$post = $api->post;

function getCurrentRecordCount( $endpoint, $get ) {
  $currentRecords = $get( $endpoint . '?fields=id&limit=1&order=id%20DESC&include_count=true' );

  if ( count( $currentRecords['content']['resource'] ) > 0 ) {
    $currentOffset = $currentRecords['content']['resource'][0]['id'];
  } else {
    $currentOffset = 0;
  }
  return $currentOffset;
}

function buildPayload( $workingOffset, $event ) {
  $workingPayload['resource'] = array();
  $xrecords = 0;
  $x = 1 + $workingOffset;

  if ( $event['request']['parameters']['xrecords'] ) {
    $xrecords = $event['request']['parameters']['xrecords'];

    if ( $workingOffset > 0 ) {
      $xrecords = $workingOffset + $xrecords;
    }

  } else {
    throw new \Exception('parameter xrecords is required');
  }

  while ( $x <= $xrecords ) {
    $record = array();
    $record['complete'] = rand( 0, 1);
    $record['name'] = 'Todo Item ' . $x;
    $workingPayload['resource'][] = $record;
    $x++;
  }

  return $workingPayload;
}

$recordsEndpoint = 'db/_table/todo';
$offset = getCurrentRecordCount( $recordsEndpoint, $get );
$payload = buildPayload( $offset, $event );
$result = $post( $recordsEndpoint, $payload );
return $result;

?>
