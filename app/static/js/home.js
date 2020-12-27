

// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: 'api/dataset',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $name = $('#name'),
        $lastModified = $('#lastModified');

    // return the API
    return {
        reset: function() {
            $lastModified.val('');
            $name.val('').focus();
        },
        update_editor: function(name, lastModified) {
            $lastModified.val(lastModified);
            $name.val(name).focus();
        },
        build_table: function(dataset) {
            let rows = ''

            // clear the table
            $('.dataset table > tbody').empty();

            // did we get a dataset array?
            if (dataset) {
                for (let i=0, l=dataset.length; i < l; i++) {
                    rows += `<tr><td class="name">${dataset[i].name}</td><td class="lastModified">${dataset[i].lastModified}</td><td>${dataset[i].filesize}</td></tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $name = $('#name'),
        $lastModified = $('#lastModified');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(name, lastModified) {
        return name !== "" && lastModified !== "";
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let name = $name.val(),
            lastModified = $lastModified.val();

        e.preventDefault();

        if (validate(name, lastModified)) {
            model.create(name, lastModified)
        } else {
            alert('Problem with first or last name input');
        }
    });

    $('#update').click(function(e) {
        let name = $name.val(),
            lastModified = $lastModified.val();

        e.preventDefault();

        if (validate(name, lastModified)) {
            model.update(name, lastModified)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let lastModified = $lastModified.val();

        e.preventDefault();

        if (validate('placeholder', lastModified)) {
            model.delete(lastModified)
        } else {
            alert('Problem with first or last name input');
        }
        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target),
            name,
            lastModified;

        name = $target
            .parent()
            .find('td.name')
            .text();

        lastModified = $target
            .parent()
            .find('td.lastModified')
            .text();

        view.update_editor(name, lastModified);
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));
