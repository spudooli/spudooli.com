$('#search-box').on('input', function () {
    $.get('/admin/checkin-search', { q: $(this).val() }, function (data) {
        // Update your search results here
        // For example, you can create a dropdown list with the results

        $('#search-results').html(data);
    });
});
