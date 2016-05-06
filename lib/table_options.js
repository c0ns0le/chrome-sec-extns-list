var st; //For debuggin only
$(document).ready(function() {
  var data = [], html = $.trim($("#template").html()), template = Mustache.compile(html);
  var view = function(record, index){
    record['updated'] = record['updated'].substring(0,10)
    record['created'] = record['created'].substring(0,10)
    return template({record: record, index: index});
  };
  var $summary = $('#summary');
  var $found = $('#found');

  $('#found').hide();

  var callbacks = {
    pagination: function(summary){
      if ($.trim($('#st_search').val()).length > 0){
        $found.text('Found : '+ summary.total).show();
      }else{
        $found.hide();
      }
      $summary.text( summary.from + ' to '+ summary.to +' of '+ summary.total +' entries');
    },

  }

  st = StreamTable('#stream_table',
    { view: view,
      per_page: 10,
      data_url: 'data/export.json',
      stream_after: 0.5,
      fetch_data_limit: 100,
      callbacks: callbacks,
      pagination: {span: 5, next_text: 'Next &rarr;', prev_text: '&larr; Previous'}
    },
   data);

});
