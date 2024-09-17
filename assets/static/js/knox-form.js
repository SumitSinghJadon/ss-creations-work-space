class KnoxSelect {
    constructor() { this.document = $(document); }

    kf_creator(element) {
        const wrapper = element.closest(".knox-form-input").addClass("relative");
        const searchBox = $("<input>").addClass("kf-select-search").attr({
            "type":"search",
            "disabled" : element.attr("disabled"),
            "readonly" : element.attr("readonly"),
            "required" : element.attr("required"),
        });
        element.removeAttr("required");
        const list = $("<list>").addClass("ks-list join join-vertical hidden absolute left-0 w-full border max-h-[200px] overflow-auto bg-base-100 z-[99]");
        list.attr("multiple", element.attr("multiple") ? true : false)

        element.find("option").each(function(){
            const oText = $(this).text();
            const oValue = $(this).val();
            const option = $("<input>").attr({
                "type" : "checkbox",
                "value" : oValue, 
                "aria-label" : oText,
                "checked" : $(this).prop("selected"),
                "disabled" : $(this).prop("disabled"),
                "class" : "btn btn-sm join-item w-full justify-start font-base font-medium"
            });
            list.append(option);
        });
        
        element.after(searchBox);
        element.after(list);
        element.height(0).width(0).attr('tabindex', "0");
        return wrapper;
    }

    kf_select_show(element){
        const self = this;
        element.find(".kf-select-search").on("focus click focusin input", function(){
            const list = element.find("list");
            if (list.is(":hidden")) {
                const inputOffset = $(this).offset();
                const windowHeight = $(window).height();
                const listHeight = list.outerHeight();
                const inputHeight = $(this).outerHeight();
                const spaceBelow = windowHeight - (inputOffset.top + inputHeight);

                list.css("top", spaceBelow < listHeight ? -listHeight : inputHeight);
                list.show().find("input:hidden").show();
            }
        });
    }

    kf_select_filter(element){
        const self = this;
        this.document.on("input", ".kf-select-search", function(){
            const inputValue = $(this).val().toUpperCase();
            
            element.find("list input").each(function(){
                const oText = $(this).attr("aria-label").toUpperCase();
                $(this).toggle(oText.indexOf(inputValue) > -1);
            });
        });

        // Clear selected values on click clear button
        this.document.on("search", ".kf-select-search", function(){
            if ($(this).val() === '') {
                element.find("list input:checked").prop("checked", false);
            } 
        });
    }

    kf_set_value(element) {
        let kf_selected_string = "";
        const valuesList = [];
        element.find("list input:checked").each(function(){
            const iText = $(this).attr("aria-label");
            const iValue = element.val() || $(this).val();
            kf_selected_string += (kf_selected_string ? "  |  " : "") + iText;
            valuesList.push(iValue);
        });
        element.find(".knox-select").val(valuesList).change();
        element.find(".kf-select-search").val(kf_selected_string);
        element.find("list").hide();
    }

    kf_select_hide(element) {
        const self = this;
        element.find(".kf-select-search").focusout(function() {
            const list = element.find("list");
            if (!list.is(":hover")){ 
                list.hide();
                // self.kf_set_value(element);
            }
        });

        element.find("list").mouseleave(function() {
            const filter_input = $(this).closest(".knox-select").find(".kf-select-search");
            if (!filter_input.is(":focus")) {
                $(this).hide();
                // self.kf_set_value(element);
            }
        });
    }

    kf_select_conf(element){
        const self = this;
        const searchInput = element.find(".kf-select-search");
        const optionList = element.find("list");
        const options = optionList.find("input");
        
        // Customize Options
        const name = searchInput.attr("name");
        options.addClass("join-item btn btn-sm").attr("name", name);
        searchInput.removeAttr("name");
        
        // Set Open Offset
        optionList.addClass("join join-vertical absolute left-0 w-full border max-h-[200px] overflow-auto");
        optionList.hide();

        options.on("change", function(){
            if (!optionList.attr("multiple")) {
                optionList.find("input").not(this).prop("checked", false);
            }
            self.kf_set_value(element);
        });
    }

    refresh(element) {
        element = this.kf_creator(element);
        this.kf_select_show(element);
        this.kf_select_filter(element);
        this.kf_set_value(element);
        this.kf_select_hide(element);
        this.kf_select_conf(element);
    }

    refreshAll() {
        const self = this;
        $(".knox-form-input .knox-select").each(function(){
            self.refresh($(this));
        });
    }
}

class KnoxInput {
    kf_number_input(element) {
        element.on("keyup", function(){
            let iValue    = parseInt($(this).val());
            let maxValue  = parseInt($(this).attr("max"));
            let minValue  = parseInt($(this).attr("min"));

            if (iValue && maxValue && iValue > maxValue) {
                $(this).val(maxValue).trigger("input")
            } else if (iValue && minValue && iValue < minValue) {
                $(this).val(minValue).trigger("input")
            }
        })
    }

    kf_date_input(element, time=false) {
        element.addClass("ki-date")
        const parsedDisabledDates = JSON.parse(element.attr("disable") || "[]");
        const parsedEnableDates = JSON.parse(element.attr("enable") || "[]");
        const isSundayFalse = element.attr("sunday");
        const sundayList =  isSundayFalse == 'false' ? [function(date) { return (date.getDay() === 0) }] : [];
        const gt = element.attr("gt");

        const config = {
            dateFormat: "d-m-Y",
            altFormat: "Y-m-d",
            disable : [...parsedDisabledDates, ...sundayList],
            enable : parsedEnableDates
        }
        
        if (time){
            config.dateFormat = "d-m-Y H:i";
            config.altFormat = "Y-m-d H:i";
            config.enableTime = true;
        }

        for (let key in config) {
            if (Array.isArray(config[key]) && config[key].length === 0) { delete config[key];}
        }
        let flatpickrInstance = element.flatpickr(config);

        let gt_input = $(`#${gt}`).on("change", function(){
            let minDate = $(this).val();
            flatpickrInstance.set("minDate", minDate);
        });
    }

    kf_file_input(element) {
        function validateExtension(input){
            var fileName = input.val();
            var acceptedTypes = input.attr('accept');
            if (acceptedTypes){
                acceptedTypes = acceptedTypes.split(',').map(function(item) {
                    return item.trim().substring(1); // Removing leading space and dot
                });
                
                if (fileName.length > 0) {
                    var fileType = fileName.split('.').pop().toLowerCase();
                    if ($.inArray(fileType, acceptedTypes) == -1) {
                        alert('Please select a file with ' + acceptedTypes.join(', ') + ' extension.');
                        input.val('');
                        return false;
                    }
                }
            }
            return true;
        }

        function validateSize(input) {
            const maxSize = input.attr('max-size');
            if (maxSize){
                var maxSizeKB = parseInt(maxSize); // Maximum file size in KB
                var fileSize = 0;
                if (input[0].files && input[0].files.length > 0) {
                    fileSize = input[0].files[0].size / 1024; // File size in KB
                }
                if (fileSize > maxSizeKB) {
                    let maxSizeMB = maxSizeKB / 1024
                    alert('File size exceeds the maximum allowed size of ' + maxSizeKB + ' KB (' + maxSizeMB + ' MB).');
                    input.val('');
                    return false;
                }
            }
            return true;
        }

        function setImagePreview(input, imgPreview) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    imgPreview.attr('src', e.target.result);
                }
                reader.readAsDataURL(input.files[0]);
            }
        }

        function setImagePreviewLarge(input, imgPreview){
            imgPreview.click(function(){
                if (input.val() !== '') {
                    const img_wrapper = $("<div>").addClass("w-full h-screen p-2 absolute bg-base-100 top-0 left-0 overflow-hidden");
                    const closeButton = $("<button>").attr({
                        "type" : "button",
                        "class" : "absolute btn btn-sm btn-error top-4 right-4 z-40 kf-largeImgPreview",
                    }).text("Close Preview");
                    const image = $("<img>").attr({
                        "class" : "max-w-full max-h-[100%] object-cover mx-auto",
                        "src" : $(this).attr("src")
                    })
                    img_wrapper.append(image);
                    img_wrapper.append(closeButton);
                    $("body").append(img_wrapper);

                    $(document).on("click", ".kf-largeImgPreview", function(){
                        img_wrapper.remove();
                    })

                    return false;
                }
            })
        }

        // File Extension Validation
        element.on("change", function(){
            const input = $(this);
            validateExtension(input);
            validateSize(input);
            const imgPreview = input.closest(".knox-form-input").find("img.kf-img-preview");
            if (imgPreview.length){
                setImagePreview(this, imgPreview); // $(this) not supported
                setImagePreviewLarge(input, imgPreview);
            } 
        })
    }

    refresh(element) {
        let iType = $(element).attr("type");

        if (iType == 'number') {
            this.kf_number_input(element);
        } else if (iType == 'date') {
            this.kf_date_input(element);
        } else if (iType == 'datetime') {
            this.kf_date_input(element, true);
        } else if (iType == 'file') {
            this.kf_file_input(element);
        }

        // if (this.queryParams) autoSetValue(element)
    }

    refreshAll() {
        const self = this;
        $(".knox-form-input .knox-input").each(function(){
            self.refresh($(this));
        });
    }
}

class KnoxTable {
    sortTable(table) {
        function getCellValue(row, index){
            let value = $(row).find('td,th').eq(index).text().trim();
            return value;
        }

        function compareValues(a, b, sortType, sortOrder) {
            function parseDate(dateStr) {
                const parts = dateStr.split('-');
                return new Date(parts[2], parts[1] - 1, parts[0]);
            }

            let aValue = a;
            let bValue = b;
            let isNumeric = false;

            if (sortType === "number") {
                aValue = parseFloat(aValue.replace(/[^0-9.-]+/g, ""));
                bValue = parseFloat(bValue.replace(/[^0-9.-]+/g, ""));
                isNumeric = true;
            } else if (sortType === 'date' || sortType === 'datetime') {
                aValue = parseDate(aValue);
                bValue = parseDate(bValue);
            }

            if (sortOrder === 'asc') {
                return isNumeric ? aValue - bValue : aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
            } else {
                return isNumeric ? bValue - aValue : bValue < aValue ? -1 : bValue > aValue ? 1 : 0;
            }
        }

        const thead = table.find("thead");
        const tbody = table.find("tbody");
        const rows = table.find("tbody tr");

        thead.find("th").not(".no-sort").click(function(){
            const th = $(this);
            const index = th.index();
            const sortType = th.data("sort");
            const sortOrder = th.data('order') || 'asc';
            
            rows.sort(function(a, b){
                const aValue = getCellValue(a, index);
                const bValue = getCellValue(b, index);

                const compareValue = compareValues(aValue, bValue, sortType, sortOrder);
                return compareValue;
            })
            const ascIcon = ' <i class="fa-light fa-arrow-down-short-wide"></i>';
            const descIcon = ' <i class="fa-light fa-arrow-up-wide-short"></i>';
            let thIcon = sortOrder === 'desc' ?  descIcon: ascIcon;
            th.html(th.text() + thIcon);
            th.data('order', sortOrder === 'desc' ? 'asc' : 'desc');
            tbody.append(rows);
        })
    }

    columnTotal(table){
        const self = this;
        const tbody = table.find("tbody");
        // const tfoot = table.find("tfoot");
        const rows = tbody.find("tr:visible");

        table.find(".kt-col-total").each(function () {
            $(this).addClass("w-full text-right");
            let sumOfCol = 0;
            const columnIndex = $(this).attr("target-col") || $(this).closest('td').index();
            
            rows.each(function () {
                const colVal = $(this).children().eq(columnIndex).text();
                const colInput = $(this).children().eq(columnIndex).find("input:visible, select:visible");
                if (colInput.length > 0) {
                    colInput.off("input");
                    colInput.on("input", function(){
                        self.columnTotal(table);
                    })
                }
                sumOfCol += parseInt(colVal, 10) || parseFloat(colVal) || parseFloat(colInput.val()) || 0;
            });
            $(this).text(sumOfCol);
        });

        // Count of visible Rows
        table.find(".kt-row-count").text(rows.length)
        table.find(".kt-row-count").val(rows.length);
    }

    addRow(table) {
        const self = this;
        table.on("click", ".addRow", function(){
            const newRow = $(this).closest('tr').clone(); // Clone the row
            $(this).closest('tr').after(newRow); // Append the new row
            // Re-index the serial numbers
            table.find('tbody tr').each(function(index) {
                $(this).find('.sr').text(index + 1);
            });
            self.refreshInput(newRow);
            self.columnTotal(table);
        });
    }

    delRow(table) {
        table.on("click", ".delRow", function(){
            if ($(table).find("tbody tr").length > 1){
                $(this).closest('tr').remove(); // Remove the row
                // Re-index the serial numbers
                table.find('tbody tr').each(function(index) {
                    $(this).find('.sr').text(index + 1);
                });
                self.refreshInput(table);
                self.columnTotal(table);
            }
        });
    }

    tableSearch(table) {
        const self = this;
        const searchInput = table.closest(".knox-table-wrapper").find(".knox-table-search");
        const tbody = table.find("tbody");
        const tfoot = table.find("tfoot");
        const rows = tbody.find("tr");
        
        searchInput.on("input", function(){
            const searchText = $(this).val().trim().toLowerCase();
            rows.each(function(){
                const rowText = $(this).text().toLocaleLowerCase();
                $(this).toggle(rowText.includes(searchText));
            })
            self.columnTotal(table);
        })
    }            

    columnSearch(table) {
        const self = this;
        const tbody = table.find("tbody");
        const tfoot = table.find("tfoot");
        const rows = table.find("tbody tr");
        
        tfoot.find(".kt-col-search").on("input", function(){
            const columnIndex = $(this).closest('td').index() + 1;
            const searchText = $(this).val().trim().toLowerCase();
            
            rows.each(function () {
                const cellText = $(this).find('td:nth-child(' + columnIndex + ')').text().toLowerCase();
                $(this).toggle(cellText.includes(searchText));
            });
            self.columnTotal(table);
        })
    }
    
    exportToExcel(table) {
        const self = this;
        const thead = table.find("thead");
        const tbody = table.find("tbody");
        const downloadBtn = table.closest(".knox-table-wrapper").find(".kt-export-btn");

        downloadBtn.click(function(){
            const tbodyRow = tbody.find("tr:visible");
            const headers = [];
            const data = [];

            // Get Headers
            thead.find("tr").children().not(".no-export").each(function(index){
                headers.push({ index : index, text: $(this).text() })
            });

            // Get Data
            tbodyRow.each(function(){
                let rowData = []
                $(this).children().not(".no-export").each(function(index){
                    rowData.push($(this).text())
                });
                data.push(rowData);
            })

            // Crate Workbook
            const wb = XLSX.utils.book_new();
            const ws = XLSX.utils.aoa_to_sheet([headers.map(header => header.text)].concat(data));
            XLSX.utils.book_append_sheet(wb, ws, "Sheet 1");
            const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'binary' });
            
            function s2ab(s) {
                const buf = new ArrayBuffer(s.length);
                const view = new Uint8Array(buf);
                for (let i = 0; i != s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
                return buf;
            }

            const tableName = table.attr("export-name") || "Table_export";
            saveAs(new Blob([s2ab(wbout)], { type: "application/octet-stream" }), `${tableName}.xlsx`);
        })
    }

    refreshInput(element) {
        element.find(".kf-select-search, .ks-list").remove();
        element.find("select, input, textarea").val('');
        element.find("input").removeClass("flatpickr-input")
        
        const knoxInput = new KnoxInput();
        const knoxSelect = new KnoxSelect();
        
        element.find(".knox-input").each(function(){
            let input = $(this);
            if (input.hasClass("ki-date")){
                input.attr("type", "date")
            } else if (input.hasClass("ki-datetime")) {
                input.attr("type", "datetime")
            }
            knoxInput.refresh(input);
        });
        
        element.find(".knox-select").each(function(){
            knoxSelect.refresh($(this));
        });
    }

    refresh(table) {
        this.addRow(table);
        this.delRow(table);
        this.sortTable(table);
        this.tableSearch(table);
        this.columnTotal(table); 
        this.columnSearch(table);
        this.exportToExcel(table);
    }

    refreshAll() {
        self = this;
        $(".knox-table").each(function(){
            self.refresh($(this));
        })
    }
}

class KnoxFormDesign {
    wrapperClass = "relative";
    baseInputClass = "input input-bordered input-sm w-full px-2 focus:border-primary placeholder-shown:border-base-300 valid:input-success invalid:input-error focus-within:!outline-none";
    peerInputClass = "input-success min-h-11 pt-4 pb-0.5 peer";
    labelClass = "absolute cursor-text text-success text-xs duration-200 origin-[0] start-4 top-1 peer-focus:top-1 peer-placeholder-shown:top-3 peer-focus:text-xs peer-focus:text-primary peer-placeholder-shown:text-current peer-placeholder-shown:text-sm";
    tableClass = "table table-xs !text-base w-full [&>*_th]:border [&>*_th]:border-base-300 [&>*_td]:border [&>*_td]:border-base-300";
    tableHeaderClass = "bg-base-200 border border-base-300 border-b-0 w-full p-1 px-3 flex justify-between";
    tfootInputClass = "rounded-none border-none knox-input bg-base-200";
    tableInputClass = "w-full rounded-none";

    knoxInputDesign(element) {
        const wrapper = element.closest(".knox-form-input");
        const input = element;
        const label = element.closest("label");
        const labelText = label.find(".label-text");
        const imgPreview = wrapper.find(".kf-img-preview");

        // File input
        if (element.attr("type")=='file') {
            if (labelText.length) {
                input.addClass("w-0 h-0 opacity-0");
                wrapper.addClass("w-full h-full")
                label.addClass(this.baseInputClass + " min-h-11 !flex");
                labelText.addClass("flex flex-col justify-between pb-0.5");
                let pathDiv = $("<span>").addClass("kf-file-path text-xs");
                // Show selected file path if already selected on page page.
                input.val() ? pathDiv.text(input.val()) : pathDiv.text("Choose a file");
                labelText.append(pathDiv);
            } else {
                input.addClass("file-input file-input-sm file-input-bordered w-full")
            }
            // Image File Input
            if (imgPreview.length) {
                label.addClass("!pl-0");
                labelText.addClass("pl-1");
                imgPreview.addClass("btn btn-md btn-square h-11");
            }
        }
        // Other Input 
        else {
            wrapper.addClass(this.wrapperClass);
            input.addClass(this.baseInputClass);
    
            if (label.length){
                input.addClass(this.peerInputClass).attr("placeholder", " ");
                labelText.addClass(this.labelClass);
            }
        }
    }

    knoxSelectDesign(element) {
        const wrapper = element.closest(".knox-form-input").addClass(this.wrapperClass);
        const select = element.addClass("absolute bottom-1 left-1/2")
        const input = element.closest(".knox-form-input").find(".kf-select-search").addClass(this.baseInputClass);
        const label = element.closest(".knox-form-input").find(".label-text");

        if (label.length){
            input.addClass(this.peerInputClass).attr("placeholder", " ");
            label.addClass(this.labelClass);
        }
    }

    knoxTableDesign(element) {
        const table = element;
        const tableWrapper = table.closest(".table-wrapper");
        const tableMainWrapper = table.closest(".knox-table-wrapper");
        const tableHeader = tableMainWrapper.find(".table-header-wrapper")
        const thead = table.find("thead");
        const tbody = table.find("tbody");
        const tfoot = table.find("tfoot");
        const tableInput = table.find("input, select, textarea");
        const tfootInput = tfoot.find("input, select, textarea");
        const tableFilterWrapper = tableMainWrapper.find(".table-filter-wrapper")
        const isSmallTable = table.hasClass("table-xs");

        tableHeader.addClass(this.tableHeaderClass);
        table.addClass(this.tableClass)
        tableInput.closest("th, td").addClass("!p-0");
        tableInput.addClass(this.tableInputClass);
        tfootInput.addClass(this.tfootInputClass).attr("placeholder", "Search...");
        thead.find("tr").addClass("bg-base-200 sticky top-0");
        tfoot.find("tr").addClass("bg-base-200 sticky bottom-0");

        // Toggle TableMainWrapper
        tableMainWrapper.find(".table-filter-toggle").click(function(){
            tableFilterWrapper.slideToggle();
        })

        if (isSmallTable) {
            thead.find("th, td").addClass("p-2")
        }
    }

    refreshInput(element) {
        if (element.hasClass("knox-input")){
            this.knoxInputDesign(element);
        } else if (element.hasClass("knox-select")){
            this.knoxSelectDesign(element);
        }
    }

    refreshAll() {
        const self = this;
        $(".knox-table").each(function(){
            self.knoxTableDesign($(this));
        })

        $(".knox-input, .knox-select").each(function(){
            self.refreshInput($(this));
        })
    }
}

function knoxForm() {
    const knoxSelect = new KnoxSelect().refreshAll();
    const knoxInput = new KnoxInput().refreshAll();
    const knoxTable = new KnoxTable().refreshAll();
    const knoxDesign = new KnoxFormDesign().refreshAll();
}

$(document).ready(function(){
    knoxForm();
});



// Function Ad Plugin
// KnoxSelect
$.fn.kf_select_refresh = function() {
    const element = $(this);
    const wrapper = element.closest(".knox-form-input");
    wrapper.find("list").remove();
    wrapper.find(".kf-select-search").remove();
    return this.each(function() {
        const knoxSelect = new KnoxSelect();
        const knoxDesign = new KnoxFormDesign();
        knoxSelect.refresh(element);
        knoxDesign.refreshInput(element);
    });
};

