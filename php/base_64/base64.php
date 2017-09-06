<?php
if ( event['request']['payload']['data'] ) {
  $data = $event['request']['payload']['data'];
} else {
  $data = '';
}

if ( $event['resource'] ) {
  if ( $event['resource'] = 'encode' ) {
    $data = base64_encode($data);
  } elseif ( $event['resource'] = 'decode' ) {
    $data = base64_decode($data);
  }
}

return $data;
?>
