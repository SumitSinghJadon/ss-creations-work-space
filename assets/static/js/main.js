function getCurrentDateTime() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    // Format: YYYY-MM-DDTHH:MM (required by datetime-local input)
    return `${year}-${month}-${day}T${hours}:${minutes}`;
}


$(document).ready(function () {
    $('.onlyNumberField').on('keydown', function(event) {
        var maxLength = $(this).data('max-length'); // Get the maximum length from data attribute
        var key = event.key;
        
        // Check if the pressed key is 'e', '+', or '-' or if the maximum length is reached
        if ((key === 'e' || key === '+' || key === '-' || $(this).val().length >= maxLength) && event.code !== 'Backspace' && event.code !== 'Delete') {
            // Prevent the default action (typing the character)
            event.preventDefault();
        }
    });
    
    //for disabling user to select back date
    $(".from_date").on("change",function(){
        $(".till_date").attr("min",$(this).val())
    })

    // append * in label if input is required
    $("form").find("select, input").each(function () {
        if ($(this).prop('required')) {
            $(this).closest('label').find(".label-text").append(
                "<span class='text-error font-bold'> *</span>"
            )
        }
    })

    // Animation on scroll / Load 
    AOS.init({
        once: true,
        offset : 0
    });
    // AOS.refresh();
})


// HTML data tables
$(document).ready(function () {
    // {% block dt_config %}
    window.datatable = $(".data-table").DataTable({
        lengthMenu: [[50, 100, 500, -1],[50, 100, 500, 'All']],
        columnDefs: [
            { targets: 'dt-nosort', orderable: false }
        ]
    });

    // {% endblock dt_config %}

    // Refine data-table design
    $(".dataTables_length select").addClass('select select-xs select-bordered rounded').prependTo(".dt-filter-top");
    $(".dataTables_filter input").addClass('input input-xs input-bordered rounded').attr(
        'placeholder', 'search in table...'
    ).prependTo(".dt-filter-top");
    $(".dataTables_info, .dataTables_paginate").prependTo(".dt-filter-botom");
    $(".dataTables_length, .dataTables_filter").remove();

    // Align tbody text if thead is in center
    try{
        $('thead tr').find('th').each(function (index) {
            const thClasses = $(this).attr('class').split(' ');
            const relevantClasses = thClasses.filter(cls => cls === '!text-right' || cls === '!text-center');
            relevantClasses.forEach(function (cls) {
                $('tbody tr').each(function () {
                    const $td = $(this).find('td, th').eq(index);
                    if (cls) { $td.addClass(cls); }
                });
            });
        });
    } catch(eer) {}

    // Add search field in each column
    $(".data-table thead tr th").each(function(){
        var isSortable = !$(this).hasClass('dt-nosort');
        var isSearchable = $(this).hasClass('dt-nosearchable');
        var tfoot = $(".data-table tfoot tr")
        var input = "<th class='!p-1'><input class='input input-xs input-bordered w-full rounded' placeholder='search'></th>";

        if (isSearchable) {
            $(tfoot).append("<th class='!p-1'></th>")
        } else {
            $(tfoot).append(input)
        }
    })

    // Set filter function in every search input
    $(".data-table tfoot tr th").each(function (index) {
        var isSearchable = index < datatable.columns().header().length && !$(this).hasClass('dt-nosearchable');

        if (isSearchable) {
            $(this).find('input').on('keyup', function () {
                datatable.column(index).search($(this).val()).draw();
            });
        }
    });
})


// HTML form 
$(document).ready(function(){
    // Form float level
    $(".float-input-label input, .float-input-label select").focusin(function() {
        $(this).closest("label").addClass("floated-label");
        $(this).addClass("!input-primary");
    })

    $(".float-input-label input, .float-input-label select").on('focusout', function() {
        if (!$(this).val()) {
            $(this).closest("label").removeClass("floated-label");
        }
        $(this).removeClass("!input-primary");
    })

    $(".float-input-label select").on('change', function() {
        if (!$(this).val()) {
            $(this).closest("label").removeClass("floated-label");
        } else {
            $(this).closest("label").addClass("floated-label");
        }
        $(this).removeClass("!input-primary");
    })

    // Check checkbox value on update form
    $("input[type=checkbox]").each(function(){
        if ($(this).attr('data-checked')) {
            let chk_val = $(this).data('checked');
            $(this).prop('checked', chk_val)
        }
    })

    // select-2 
    $("#form-save-btn").on("click", function(){
        $('form').find("#submit-btn").click();
    })

    // select-2 input customization
    $(".select-2").select2();
    
    // $(".select-2, select").each(function(){
    //     $(this).change();
    // });

    $(".select2-container, .select-bordered, .selection, .select2-selection").addClass('!h-full !w-full');
    $(".select2-selection").addClass('text-input');
    $('.float-input-label').find(".select2-selection__rendered").addClass('!pt-1');
    $('.float-input-label').find(".select2-selection__arrow").addClass('!top-1.5');

    // Search in table
    $('.search-in-table').on('change', function () {
        let index = $(this).data("col-index")
        let value = $(this).find("option:selected").text();
        if (!$(this).val()){ value = '' }
        datatable.column(index).search(value).draw();
    });

    document.getElementById('application_form').addEventListener('submit', function(event) {
        event.preventDefault();
        showLoadingOverlay();
        
        const formData = new FormData(this);
        const formAction = this.getAttribute('action');
        fetch(formAction, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            show_alert('success','Data has been successfully saved!')
            hideLoadingOverlay()
            setTimeout(function(){window.location.reload()},400)
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function showLoadingOverlay() {
        document.getElementById('loadingOverlay').style.display = 'block';
    }

    function hideLoadingOverlay() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }
})

