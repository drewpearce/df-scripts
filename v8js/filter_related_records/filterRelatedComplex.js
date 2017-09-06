var lodash = require('lodash.min.js'); // Bring in lodash for each
var service_name = 'db'; // Insert the name of the service related to this event
var table_name = 'contact'; // Insert the name of the table related to this event.
var parameters = event.request.parameters; // Get parameters
var parameters_keys = Object.keys(parameters); // Get parameter names

function buildRelatedURL(param_key) {
    var related_schema_url = service_name + '/_schema/' + table_name + '/_related/' + param_key.replace('_filter', '');
    var related_schema = platform.api.get(related_schema_url);
    var ref_service_id = related_schema.content.ref_service_id;
    var ref_service_url = 'system/service/' + ref_service_id + '?fields=name';
    var ref_table = related_schema.content.ref_table;
    var ref_service = platform.api.get(ref_service_url);
    var ref_service_name = ref_service.content.name;
    var related_url = ref_service_name + '/_table/' + ref_table;
    return related_url
}
// Check if the call contains a related request
if ('related' in parameters) {
    // Check for *_filter parameter names
    var related_filters = [];
    lodash._.each(parameters_keys, function(param) {
        if (param.includes('_filter')) {
            related_filters.push(param);
        }
    });

    // If any related filters were passed:
    if (related_filters.length > 0) {
        var related_endpoint = buildRelatedURL(related_filters[0]);
        
    }
    /*
    if ('residents_by_homes_id' in event.request.parameters.related) {
        if ('residents_by_homes_id_filter' in event.request.parameters) {
            var url = 'localdata/_table/residents?fields=id&filter=' + event.request.parameters.residents_by_homes_id_filter;
            result = platform.api.get(url);
            if (result.status_code == 200) {
                var ids = [];
                lodash._.each(result.content.resource, function(record){
                    ids.push(record.id);
                });
                lodash._.each(event.response.content.resource, function(parent_record){
                    lodash._.each(parent_record.residents_by_homes_id, function(child_record, index){
                        if (!ids.includes(child_record.id)){
                            delete parent_record.residents_by_homes_id[index];
                        }
                   });
                });
            }
        }
    }*/
}
